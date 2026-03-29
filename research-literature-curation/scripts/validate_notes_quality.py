from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REQUIRED_SECTIONS = [
    "Summary",
    "Key Claims",
    "Method / Argument",
    "Evidence and Citation Use",
    "Caveats",
]

SNIPPETS_SECTION = "Reading Evidence Snippets"

PLACEHOLDER_TEXT = {
    "",
    "-",
    "todo",
    "tbd",
    "na",
    "n/a",
    "...",
    "待补",
    "待补充",
    "待完善",
    "暂无",
    "none",
}

HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
BULLET_RE = re.compile(r"^\s*-\s*(.*)$")


@dataclass
class PaperCheck:
    paper_id: str
    notes_path: str
    ok: bool
    issues: list[str]
    section_bullet_counts: dict[str, int]


def normalize_text(s: str) -> str:
    return s.strip().lower()


def is_placeholder_bullet(text: str) -> bool:
    t = normalize_text(text)
    if t in PLACEHOLDER_TEXT:
        return True
    # Punctuation-only lines should not count as meaningful notes.
    if t and all(ch in "-_*~.。，、；;:：()[]{}<>《》\"'` " for ch in t):
        return True
    return False


def parse_sections(lines: Iterable[str]) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for raw in lines:
        line = raw.rstrip("\n")
        m = HEADING_RE.match(line.strip())
        if m:
            current = m.group(1).strip()
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return sections


def meaningful_bullets(section_lines: list[str]) -> list[str]:
    bullets: list[str] = []
    for line in section_lines:
        m = BULLET_RE.match(line)
        if not m:
            continue
        text = m.group(1).strip()
        if is_placeholder_bullet(text):
            continue
        bullets.append(text)
    return bullets


def check_note(
    paper_id: str,
    notes_path: Path,
    min_bullets: int,
    min_snippets: int,
    require_snippets: bool,
) -> PaperCheck:
    issues: list[str] = []
    counts: dict[str, int] = {}

    if not notes_path.exists():
        return PaperCheck(
            paper_id=paper_id,
            notes_path=str(notes_path),
            ok=False,
            issues=["notes.md missing"],
            section_bullet_counts={},
        )

    text = notes_path.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        return PaperCheck(
            paper_id=paper_id,
            notes_path=str(notes_path),
            ok=False,
            issues=["notes.md is empty"],
            section_bullet_counts={},
        )

    sections = parse_sections(text.splitlines())
    total_meaningful = 0

    for section in REQUIRED_SECTIONS:
        if section not in sections:
            issues.append(f"missing section: {section}")
            counts[section] = 0
            continue
        bullets = meaningful_bullets(sections[section])
        counts[section] = len(bullets)
        total_meaningful += len(bullets)
        if len(bullets) < min_bullets:
            issues.append(f"section '{section}' has only {len(bullets)} meaningful bullets (< {min_bullets})")

    if require_snippets:
        if SNIPPETS_SECTION not in sections:
            issues.append(f"missing section: {SNIPPETS_SECTION}")
            counts[SNIPPETS_SECTION] = 0
        else:
            bullets = meaningful_bullets(sections[SNIPPETS_SECTION])
            counts[SNIPPETS_SECTION] = len(bullets)
            total_meaningful += len(bullets)
            if len(bullets) < min_snippets:
                issues.append(f"section '{SNIPPETS_SECTION}' has only {len(bullets)} snippets (< {min_snippets})")

    if total_meaningful == 0:
        issues.append("notes contain no meaningful bullets (template placeholder only)")

    return PaperCheck(
        paper_id=paper_id,
        notes_path=str(notes_path),
        ok=len(issues) == 0,
        issues=issues,
        section_bullet_counts=counts,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate per-paper notes quality and placeholder completeness.")
    parser.add_argument("--papers-root", required=True, help="Path to papers/ directory")
    parser.add_argument("--report", required=True, help="Path to markdown report")
    parser.add_argument("--json-output", default="", help="Optional JSON output path")
    parser.add_argument("--min-bullets", type=int, default=3, help="Minimum meaningful bullets per required section")
    parser.add_argument("--min-snippets", type=int, default=3, help="Minimum snippets in Reading Evidence Snippets")
    parser.add_argument("--no-require-snippets", action="store_true", help="Disable snippet section requirement")
    args = parser.parse_args()

    papers_root = Path(args.papers_root).resolve()
    report_path = Path(args.report).resolve()
    json_path = Path(args.json_output).resolve() if args.json_output else None
    require_snippets = not args.no_require_snippets

    checks: list[PaperCheck] = []
    for paper_dir in sorted([p for p in papers_root.iterdir() if p.is_dir()], key=lambda p: p.name):
        checks.append(
            check_note(
                paper_id=paper_dir.name,
                notes_path=paper_dir / "notes.md",
                min_bullets=args.min_bullets,
                min_snippets=args.min_snippets,
                require_snippets=require_snippets,
            )
        )

    failed = [c for c in checks if not c.ok]
    passed = [c for c in checks if c.ok]

    lines = [
        "# Notes Quality Report",
        "",
        f"- papers_root: `{papers_root}`",
        f"- total: {len(checks)}",
        f"- passed: {len(passed)}",
        f"- failed: {len(failed)}",
        f"- min_bullets: {args.min_bullets}",
        f"- require_snippets: {require_snippets}",
        "",
    ]

    if failed:
        lines.append("## Failed Papers")
        lines.append("")
        for item in failed:
            lines.append(f"### {item.paper_id}")
            lines.append(f"- notes: `{item.notes_path}`")
            for issue in item.issues:
                lines.append(f"- issue: {issue}")
            if item.section_bullet_counts:
                lines.append(f"- counts: `{json.dumps(item.section_bullet_counts, ensure_ascii=False)}`")
            lines.append("")
    else:
        lines.append("All paper notes passed quality checks.")
        lines.append("")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")

    if json_path is not None:
        payload = {
            "papers_root": str(papers_root),
            "total": len(checks),
            "passed": len(passed),
            "failed": len(failed),
            "checks": [
                {
                    "paper_id": c.paper_id,
                    "notes_path": c.notes_path,
                    "ok": c.ok,
                    "issues": c.issues,
                    "section_bullet_counts": c.section_bullet_counts,
                }
                for c in checks
            ],
        }
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Wrote notes quality report: {report_path}")
    if json_path is not None:
        print(f"Wrote notes quality json: {json_path}")
    return 0 if not failed else 2


if __name__ == "__main__":
    raise SystemExit(main())
