from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
NUMBERED_RE = re.compile(r"^((?:\d+\.)*\d+)\s+(.+?)\s*$")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")

PLACEHOLDER_PATTERNS = [
    "Fill in a concrete objective",
    "<source-id",
    "<query-",
    "<claim text>",
    "unresolved conflict",
    "TODO",
    "TBD",
    "???",
]

REQUIRED_PACKET_HEADINGS = [
    "## Subsection Title",
    "## Section Goal",
    "## Relevant Source IDs",
    "## Key Claims",
    "## Caveats",
]


@dataclass
class OutlineNode:
    level: int
    section_id: str
    title: str


def parse_outline_nodes(markdown: str) -> list[OutlineNode]:
    nodes: list[OutlineNode] = []
    for raw in markdown.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = HEADING_RE.match(line)
        text = m.group(2).strip() if m else line
        mm = NUMBERED_RE.match(text)
        if not mm:
            continue
        section_id = mm.group(1).strip()
        title = mm.group(2).strip()
        inferred_level = section_id.count(".") + 1
        heading_level = len(m.group(1)) if m else 0
        level = max(inferred_level, heading_level)
        nodes.append(OutlineNode(level=level, section_id=section_id, title=title))
    return nodes


def has_heading(text: str, heading: str) -> bool:
    return re.search(rf"^{re.escape(heading)}\s*$", text, flags=re.M) is not None


def cjk_ratio(text: str) -> float:
    if not text:
        return 0.0
    non_space = [ch for ch in text if not ch.isspace()]
    if not non_space:
        return 0.0
    cjk_count = sum(1 for ch in non_space if CJK_RE.match(ch))
    return cjk_count / len(non_space)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate section packet completeness and quality.")
    parser.add_argument("--outline", required=True, help="Path to refined_outline.md")
    parser.add_argument("--packets-dir", required=True, help="Directory containing section_packets")
    parser.add_argument("--min-level", type=int, default=3, help="Validate headings at or deeper than this level")
    parser.add_argument("--language", choices=["zh", "en"], default=None, help="Optional packet language lock")
    parser.add_argument("--report", default=None, help="Optional markdown output report path")
    args = parser.parse_args()

    outline_path = Path(args.outline).resolve()
    packets_dir = Path(args.packets_dir).resolve()

    outline_text = outline_path.read_text(encoding="utf-8", errors="ignore")
    nodes = [n for n in parse_outline_nodes(outline_text) if n.level >= args.min_level]

    missing_files: list[str] = []
    heading_issues: list[str] = []
    placeholder_issues: list[str] = []
    language_issues: list[str] = []

    for node in nodes:
        packet_path = packets_dir / f"{node.section_id}.md"
        if not packet_path.exists():
            missing_files.append(node.section_id)
            continue
        text = packet_path.read_text(encoding="utf-8", errors="ignore")

        for heading in REQUIRED_PACKET_HEADINGS:
            if not has_heading(text, heading):
                heading_issues.append(f"{node.section_id}: missing heading `{heading}`")

        for p in PLACEHOLDER_PATTERNS:
            if p in text:
                placeholder_issues.append(f"{node.section_id}: contains placeholder `{p}`")

        if args.language is not None:
            ratio = cjk_ratio(text)
            if args.language == "zh" and ratio < 0.12:
                language_issues.append(f"{node.section_id}: low zh ratio ({ratio:.2f})")
            if args.language == "en" and ratio > 0.35:
                language_issues.append(f"{node.section_id}: high zh ratio ({ratio:.2f})")

    total_required = len(nodes)
    missing_count = len(missing_files)
    pass_ok = not (missing_files or heading_issues or placeholder_issues or language_issues)

    report_lines = [
        "# Section Packet Validation Report",
        "",
        f"- outline: `{outline_path}`",
        f"- packets_dir: `{packets_dir}`",
        f"- min_level: `{args.min_level}`",
        f"- language_lock: `{args.language}`",
        f"- required_packets: `{total_required}`",
        f"- missing_packets: `{missing_count}`",
        f"- pass: `{pass_ok}`",
        "",
    ]

    if missing_files:
        report_lines.extend(["## Missing packet files", ""])
        report_lines.extend([f"- `{sid}.md`" for sid in missing_files])
        report_lines.append("")

    if heading_issues:
        report_lines.extend(["## Packet heading issues", ""])
        report_lines.extend([f"- {x}" for x in heading_issues])
        report_lines.append("")

    if placeholder_issues:
        report_lines.extend(["## Placeholder issues", ""])
        report_lines.extend([f"- {x}" for x in placeholder_issues])
        report_lines.append("")

    if language_issues:
        report_lines.extend(["## Language issues", ""])
        report_lines.extend([f"- {x}" for x in language_issues])
        report_lines.append("")

    if pass_ok:
        report_lines.extend(["## Result", "", "- All required packets passed checks."])

    report_text = "\n".join(report_lines) + "\n"
    if args.report:
        report_path = Path(args.report).resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report_text, encoding="utf-8")
    else:
        sys.stdout.write(report_text)

    return 0 if pass_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
