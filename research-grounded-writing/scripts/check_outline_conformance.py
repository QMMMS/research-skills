from __future__ import annotations

import argparse
import re
from pathlib import Path


MD_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
NUMBERED_PREFIX_RE = re.compile(r"^((?:\d+\.)*\d+)\s+(.+?)\s*$")
WORD_RE = re.compile(r"[a-z0-9]+")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def tokenize(text: str) -> set[str]:
    return set(WORD_RE.findall(text.lower()))


def similarity(a: str, b: str) -> float:
    aa = tokenize(a)
    bb = tokenize(b)
    if not aa and not bb:
        return 1.0
    if not aa or not bb:
        return 0.0
    return len(aa & bb) / len(aa | bb)


def parse_numbered_headings(path: Path) -> dict[str, tuple[str, int]]:
    result: dict[str, tuple[str, int]] = {}
    text = path.read_text(encoding="utf-8", errors="ignore")
    for line_no, raw in enumerate(text.splitlines(), start=1):
        line = raw.rstrip()
        if not line.strip():
            continue

        md = MD_HEADING_RE.match(line)
        text_part = md.group(2).strip() if md else line.strip()
        m = NUMBERED_PREFIX_RE.match(text_part)
        if not m:
            continue
        section_id = m.group(1).strip()
        title = m.group(2).strip()
        if section_id not in result:
            result[section_id] = (title, line_no)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Check heading conformance between refined outline and report.")
    parser.add_argument("--outline", required=True, help="Path to refined_outline.md")
    parser.add_argument("--report", required=True, help="Path to detailed_report.md / revised_report.md")
    parser.add_argument("--output", required=True, help="Path to write conformance report")
    parser.add_argument(
        "--title-sim-threshold",
        type=float,
        default=0.45,
        help="Warn when title overlap for same section id is below this threshold",
    )
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when missing/unexpected section ids are found")
    args = parser.parse_args()

    outline_path = Path(args.outline).resolve()
    report_path = Path(args.report).resolve()
    output_path = Path(args.output).resolve()

    outline = parse_numbered_headings(outline_path)
    report = parse_numbered_headings(report_path)

    outline_ids = set(outline.keys())
    report_ids = set(report.keys())

    missing = sorted(outline_ids - report_ids, key=lambda x: [int(p) for p in x.split(".")])
    unexpected = sorted(report_ids - outline_ids, key=lambda x: [int(p) for p in x.split(".")])

    drift: list[str] = []
    for sid in sorted(outline_ids & report_ids, key=lambda x: [int(p) for p in x.split(".")]):
        outline_title = outline[sid][0]
        report_title = report[sid][0]
        sim = similarity(normalize(outline_title), normalize(report_title))
        if sim < args.title_sim_threshold:
            drift.append(
                f"`{sid}` title drift: outline=`{outline_title}` vs report=`{report_title}` (sim={sim:.2f})"
            )

    lines = [
        "# Outline Conformance Report",
        "",
        f"- Outline: `{outline_path}`",
        f"- Report: `{report_path}`",
        f"- Outline heading ids: {len(outline_ids)}",
        f"- Report heading ids: {len(report_ids)}",
        f"- Missing ids: {len(missing)}",
        f"- Unexpected ids: {len(unexpected)}",
        f"- Title drift warnings: {len(drift)}",
        "",
    ]

    if missing:
        lines.append("## Missing Section IDs (in outline, not in report)")
        lines.append("")
        for sid in missing:
            title, line_no = outline[sid]
            lines.append(f"- `{sid}` `{title}` (outline line {line_no})")
        lines.append("")

    if unexpected:
        lines.append("## Unexpected Section IDs (in report, not in outline)")
        lines.append("")
        for sid in unexpected:
            title, line_no = report[sid]
            lines.append(f"- `{sid}` `{title}` (report line {line_no})")
        lines.append("")

    if drift:
        lines.append("## Title Drift Warnings")
        lines.append("")
        for item in drift:
            lines.append(f"- {item}")
        lines.append("")

    if not missing and not unexpected and not drift:
        lines.append("No conformance issues found.")
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote conformance report: {output_path}")

    if args.strict and (missing or unexpected):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
