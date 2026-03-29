from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
SECTION_ID_RE = re.compile(r"^((?:\d+\.)*\d+)\s+(.+)$")
SENTENCE_RE = re.compile(r"[。！？!?]+")


@dataclass
class SectionBlock:
    section_id: str
    title: str
    level: int
    lines: list[str]


def parse_blocks(text: str, target_depth: int) -> list[SectionBlock]:
    lines = text.splitlines()
    blocks: list[SectionBlock] = []
    current: SectionBlock | None = None

    for raw in lines:
        m = HEADING_RE.match(raw.strip())
        if m:
            heading_text = m.group(2).strip()
            sid = SECTION_ID_RE.match(heading_text)
            if sid:
                section_id = sid.group(1)
                depth = section_id.count(".") + 1
                if depth == target_depth:
                    if current is not None:
                        blocks.append(current)
                    current = SectionBlock(
                        section_id=section_id,
                        title=sid.group(2).strip(),
                        level=depth,
                        lines=[],
                    )
                    continue
                if current is not None and depth <= target_depth:
                    blocks.append(current)
                    current = None

        if current is not None:
            current.lines.append(raw)

    if current is not None:
        blocks.append(current)
    return blocks


def split_paragraphs(lines: list[str]) -> list[str]:
    paragraphs: list[str] = []
    buf: list[str] = []
    for line in lines:
        s = line.strip()
        if not s:
            if buf:
                paragraphs.append(" ".join(buf).strip())
                buf = []
            continue
        if s.startswith("#"):
            continue
        buf.append(s)
    if buf:
        paragraphs.append(" ".join(buf).strip())
    return paragraphs


def sentence_count(paragraph: str) -> int:
    return len(SENTENCE_RE.findall(paragraph))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate subsection paragraph and sentence depth.")
    parser.add_argument("--report", required=True, help="Path to report markdown")
    parser.add_argument("--target-depth", type=int, default=3, help="Section depth to validate (e.g., 3 for 1.1.1)")
    parser.add_argument("--min-paragraphs", type=int, default=2)
    parser.add_argument("--min-sentences", type=int, default=3)
    parser.add_argument("--out", default=None, help="Optional markdown output path")
    args = parser.parse_args()

    report_path = Path(args.report).resolve()
    text = report_path.read_text(encoding="utf-8", errors="ignore")
    blocks = parse_blocks(text, args.target_depth)

    issues: list[str] = []
    checked = 0
    for b in blocks:
        paragraphs = split_paragraphs(b.lines)
        checked += 1
        if len(paragraphs) < args.min_paragraphs:
            issues.append(
                f"{b.section_id} {b.title}: paragraph_count={len(paragraphs)} < {args.min_paragraphs}"
            )
            continue
        for i, p in enumerate(paragraphs, start=1):
            sc = sentence_count(p)
            if sc < args.min_sentences:
                issues.append(
                    f"{b.section_id} {b.title}: paragraph_{i}_sentences={sc} < {args.min_sentences}"
                )

    passed = len(issues) == 0
    lines = [
        "# Report Depth Validation",
        "",
        f"- report: `{report_path}`",
        f"- target_depth: `{args.target_depth}`",
        f"- min_paragraphs: `{args.min_paragraphs}`",
        f"- min_sentences_per_paragraph: `{args.min_sentences}`",
        f"- checked_sections: `{checked}`",
        f"- pass: `{passed}`",
        "",
    ]

    if issues:
        lines.extend(["## Issues", ""])
        lines.extend([f"- {x}" for x in issues])
    else:
        lines.extend(["## Result", "", "- All checked sections satisfy depth requirements."])

    output = "\n".join(lines) + "\n"
    if args.out:
        out_path = Path(args.out).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
