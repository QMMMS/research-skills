from __future__ import annotations

import argparse
import re
from pathlib import Path


HEADING_COMMANDS = (
    r"\section{",
    r"\subsection{",
    r"\subsubsection{",
    r"\paragraph{",
)


def strip_comments(line: str) -> str:
    return re.sub(r"(?<!\\)%.*$", "", line)


def is_structural_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith(HEADING_COMMANDS):
        return True
    if stripped.startswith((r"\begin{", r"\end{", r"\bibliography{", r"\bibliographystyle{", r"\label{")):
        return True
    return False


def has_citation(text: str) -> bool:
    return any(token in text for token in (r"\cite{", r"\citet{", r"\citep{", r"\citealt{", r"\citeauthor{"))


def collect_paragraphs(text: str) -> list[tuple[int, str]]:
    lines = text.splitlines()
    paragraphs: list[tuple[int, str]] = []
    buffer: list[str] = []
    start_line = 0
    in_document = False

    def flush() -> None:
        nonlocal buffer, start_line
        if not buffer:
            return
        joined = " ".join(part.strip() for part in buffer if part.strip()).strip()
        if joined:
            paragraphs.append((start_line, joined))
        buffer = []
        start_line = 0

    for idx, raw in enumerate(lines, start=1):
        line = strip_comments(raw).rstrip()
        stripped = line.strip()

        if stripped.startswith(r"\begin{document}"):
            in_document = True
            flush()
            continue
        if stripped.startswith(r"\end{document}"):
            flush()
            break
        if not in_document:
            continue

        if not line.strip():
            flush()
            continue
        if is_structural_line(line):
            flush()
            continue
        if not buffer:
            start_line = idx
        buffer.append(line)

    flush()
    return paragraphs


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit long LaTeX paragraphs that lack citations.")
    parser.add_argument("--main-tex", required=True, help="Path to main.tex")
    parser.add_argument("--output", required=True, help="Output markdown report path")
    parser.add_argument(
        "--min-chars",
        type=int,
        default=220,
        help="Minimum paragraph length to require at least one citation",
    )
    args = parser.parse_args()

    main_tex = Path(args.main_tex).resolve()
    output = Path(args.output).resolve()
    content = main_tex.read_text(encoding="utf-8", errors="ignore")
    paragraphs = collect_paragraphs(content)

    flagged: list[tuple[int, str]] = []
    for line_no, paragraph in paragraphs:
        if len(paragraph) >= args.min_chars and not has_citation(paragraph):
            flagged.append((line_no, paragraph))

    lines = [
        "# Paragraph Citation Gaps",
        "",
        f"- Main tex: `{main_tex}`",
        f"- Min chars: {args.min_chars}",
        f"- Flagged paragraphs: {len(flagged)}",
        "",
    ]

    if not flagged:
        lines.append("No long uncited paragraphs found.")
    else:
        lines.append("## Flagged")
        lines.append("")
        for line_no, paragraph in flagged:
            preview = paragraph[:240].replace("\n", " ")
            if len(paragraph) > 240:
                preview += "..."
            lines.append(f"- line {line_no}: {preview}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote paragraph citation audit to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
