from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path


UNDEFINED_CITATION_PATTERNS = [
    re.compile(r"Citation [`'\"]([^`'\"]+)[`'\"] .* undefined", re.IGNORECASE),
    re.compile(r"I didn't find a database entry for \"([^\"]+)\"", re.IGNORECASE),
]


def extract_citation_state_from_aux(aux_path: Path) -> tuple[set[str], set[str]]:
    if not aux_path.exists():
        return set(), set()
    text = aux_path.read_text(encoding="utf-8", errors="ignore")
    citations: set[str] = set()
    for match in re.finditer(r"\\citation\{([^}]*)\}", text):
        raw = match.group(1).strip()
        if not raw:
            continue
        for part in raw.split(","):
            key = part.strip()
            if key:
                citations.add(key)
    bibcites = {m.group(1).strip() for m in re.finditer(r"\\bibcite\{([^}]*)\}", text) if m.group(1).strip()}
    return citations, bibcites


def extract_undefined_citations(text: str) -> list[str]:
    summary_match = re.findall(r"Latex failed to resolve\s+(\d+)\s+citation", text, flags=re.IGNORECASE)
    if summary_match and int(summary_match[-1]) == 0:
        return []

    block_match = re.findall(
        r"Latexmk:\s+====Undefined refs and citations with line #s in \.tex file:(.*?)(?:\nReverting Windows console CPs|\Z)",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if block_match:
        keys: set[str] = set()
        for match in re.finditer(r"Citation [`'\"]([^`'\"]+)[`'\"]", block_match[-1], flags=re.IGNORECASE):
            key = match.group(1).strip()
            if key:
                keys.add(key)
        return sorted(keys)

    keys: set[str] = set()
    for pattern in UNDEFINED_CITATION_PATTERNS:
        for match in pattern.finditer(text):
            key = match.group(1).strip()
            if key:
                keys.add(key)
    return sorted(keys)


def write_citation_gap_report(report_path: Path, keys: list[str], main_tex: Path) -> None:
    lines = [
        "# Citation Gaps",
        "",
        f"- Main tex: `{main_tex}`",
        f"- Undefined citation count: {len(keys)}",
        "",
    ]
    if not keys:
        lines.append("No undefined citations found.")
    else:
        lines.append("## Missing citation keys")
        lines.append("")
        for key in keys:
            lines.append(f"- `{key}`")
        lines.append("")
        lines.append("## Suggested repair actions")
        lines.append("")
        lines.append("- Ensure `references.bib` contains matching keys.")
        lines.append("- Add eprint-based alias keys when `\\cite{arxiv-id}` is used.")
        lines.append("- Re-run export and compile after key repair.")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(cmd: list[str], cwd: Path, log_path: Path) -> int:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    log_path.write_text(
        (result.stdout or "") + "\n\n" + (result.stderr or ""),
        encoding="utf-8",
    )
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a LaTeX project using latexmk or pdflatex/bibtex.")
    parser.add_argument("--main-tex", required=True, help="Path to main.tex")
    parser.add_argument("--log", required=True, help="Path to build log")
    parser.add_argument(
        "--citation-gap-report",
        help="Path to write undefined citation report; defaults to <main-tex-dir>/citation_gaps.md",
    )
    parser.add_argument(
        "--allow-undefined-citations",
        action="store_true",
        help="Do not fail when undefined citations are detected.",
    )
    args = parser.parse_args()

    main_tex = Path(args.main_tex).resolve()
    log_path = Path(args.log).resolve()
    work_dir = main_tex.parent
    gap_report_path = (
        Path(args.citation_gap_report).resolve()
        if args.citation_gap_report
        else (work_dir / "citation_gaps.md")
    )
    aux_path = main_tex.with_suffix(".aux")

    def finalize_compile(exit_code: int) -> int:
        citations, bibcites = extract_citation_state_from_aux(aux_path)
        if citations:
            missing = sorted(citations - bibcites)
            write_citation_gap_report(gap_report_path, missing, main_tex)
            if missing and not args.allow_undefined_citations:
                print(f"Undefined citations found: {len(missing)}. See {gap_report_path}")
                return 2
            return exit_code

        if not log_path.exists():
            return exit_code
        text = log_path.read_text(encoding="utf-8", errors="ignore")
        missing = extract_undefined_citations(text)
        write_citation_gap_report(gap_report_path, missing, main_tex)
        if missing and not args.allow_undefined_citations:
            print(f"Undefined citations found: {len(missing)}. See {gap_report_path}")
            return 2
        return exit_code

    if shutil.which("latexmk"):
        code = run(
            ["latexmk", "-pdf", "-interaction=nonstopmode", "-file-line-error", main_tex.name],
            work_dir,
            log_path,
        )
        print(f"latexmk exit code: {code}")
        return finalize_compile(code)

    if not shutil.which("pdflatex"):
        log_path.write_text("No TeX compiler found. Install latexmk or pdflatex.", encoding="utf-8")
        print("No TeX compiler found.")
        return 1

    steps = [
        ["pdflatex", "-interaction=nonstopmode", main_tex.name],
    ]
    if (work_dir / "references.bib").exists() and shutil.which("bibtex"):
        steps.extend(
            [
                ["bibtex", main_tex.stem],
                ["pdflatex", "-interaction=nonstopmode", main_tex.name],
                ["pdflatex", "-interaction=nonstopmode", main_tex.name],
            ]
        )

    combined: list[str] = []
    for cmd in steps:
        result = subprocess.run(cmd, cwd=work_dir, capture_output=True, text=True)
        combined.append("$ " + " ".join(cmd))
        combined.append(result.stdout or "")
        combined.append(result.stderr or "")
        if result.returncode != 0:
            log_path.write_text("\n".join(combined), encoding="utf-8")
            print(f"Command failed: {' '.join(cmd)}")
            return result.returncode

    log_path.write_text("\n".join(combined), encoding="utf-8")
    print("Compilation finished.")
    return finalize_compile(0)


if __name__ == "__main__":
    raise SystemExit(main())
