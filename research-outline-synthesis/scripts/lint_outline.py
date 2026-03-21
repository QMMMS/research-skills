from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


MD_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
NUMBERED_PREFIX_RE = re.compile(r"^((?:\d+\.)*\d+)\s+(.+?)\s*$")
WORD_RE = re.compile(r"[a-z0-9]+")
STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "by",
    "for",
    "from",
    "in",
    "into",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}


@dataclass
class HeadingNode:
    idx: int
    line_no: int
    level: int
    section_id: str | None
    title: str
    normalized: str
    parent_idx: int | None
    next_line_no: int


def normalize_title(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def title_tokens(text: str) -> set[str]:
    return {w for w in WORD_RE.findall(text.lower()) if w not in STOPWORDS}


def parse_outline(text: str) -> tuple[list[HeadingNode], list[str]]:
    lines = text.splitlines()
    parsed: list[tuple[int, int, str | None, str]] = []
    for idx, raw in enumerate(lines):
        line = raw.rstrip()
        if not line.strip():
            continue
        md = MD_HEADING_RE.match(line)
        if md:
            level = len(md.group(1))
            head_text = md.group(2).strip()
            num = NUMBERED_PREFIX_RE.match(head_text)
            if num:
                section_id = num.group(1)
                title = num.group(2).strip()
                level = max(level, section_id.count(".") + 1)
            else:
                section_id = None
                title = head_text
            parsed.append((idx + 1, level, section_id, title))
            continue

        num_only = NUMBERED_PREFIX_RE.match(line)
        if num_only:
            section_id = num_only.group(1)
            title = num_only.group(2).strip()
            level = section_id.count(".") + 1
            parsed.append((idx + 1, level, section_id, title))

    nodes: list[HeadingNode] = []
    stack: list[HeadingNode] = []
    for i, (line_no, level, section_id, title) in enumerate(parsed):
        while stack and stack[-1].level >= level:
            stack.pop()
        parent_idx = stack[-1].idx if stack else None
        next_line_no = parsed[i + 1][0] if i + 1 < len(parsed) else len(lines) + 1
        node = HeadingNode(
            idx=i,
            line_no=line_no,
            level=level,
            section_id=section_id,
            title=title,
            normalized=normalize_title(title),
            parent_idx=parent_idx,
            next_line_no=next_line_no,
        )
        nodes.append(node)
        stack.append(node)
    return nodes, lines


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / max(1, len(a | b))


def is_similar(a: str, b: str, threshold: float) -> bool:
    na = normalize_title(a)
    nb = normalize_title(b)
    if na == nb:
        return True
    if na.startswith(nb) or nb.startswith(na):
        if min(len(na), len(nb)) >= 12:
            return True
    return jaccard(title_tokens(na), title_tokens(nb)) >= threshold


def has_body_text(node: HeadingNode, lines: list[str], heading_lines: set[int]) -> bool:
    start = node.line_no
    end = node.next_line_no
    for ln in range(start + 1, end):
        if ln in heading_lines:
            continue
        if lines[ln - 1].strip():
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint a multi-level research outline.")
    parser.add_argument("--input", required=True, help="Path to draft/refined outline markdown file.")
    parser.add_argument("--output", required=True, help="Path to write lint report markdown.")
    parser.add_argument("--min-subsections", type=int, default=2, help="Minimum immediate subsections under each top-level section.")
    parser.add_argument("--overlap-threshold", type=float, default=0.8, help="Sibling title similarity threshold.")
    parser.add_argument("--fail-on-warning", action="store_true", help="Exit non-zero when warnings exist.")
    args = parser.parse_args()

    outline_path = Path(args.input).resolve()
    report_path = Path(args.output).resolve()
    text = outline_path.read_text(encoding="utf-8", errors="ignore")
    nodes, lines = parse_outline(text)

    errors: list[str] = []
    warnings: list[str] = []

    if not nodes:
        errors.append("No headings found. Outline appears empty or unstructured.")

    by_parent: dict[int | None, list[HeadingNode]] = {}
    for node in nodes:
        by_parent.setdefault(node.parent_idx, []).append(node)

    for parent, siblings in by_parent.items():
        seen: dict[str, list[HeadingNode]] = {}
        for node in siblings:
            seen.setdefault(node.normalized, []).append(node)
        for norm, dup_nodes in seen.items():
            if len(dup_nodes) > 1:
                lines_info = ", ".join(str(n.line_no) for n in dup_nodes)
                errors.append(f"Duplicate sibling heading `{norm}` under parent `{parent}` at lines: {lines_info}.")

    heading_lines = {n.line_no for n in nodes}
    child_count: dict[int, int] = {n.idx: 0 for n in nodes}
    for n in nodes:
        if n.parent_idx is not None:
            child_count[n.parent_idx] += 1

    for n in nodes:
        if child_count[n.idx] == 0 and not has_body_text(n, lines, heading_lines):
            errors.append(
                f"Heading at line {n.line_no} has neither subsection nor body text: `{n.title}`."
            )

    for n in nodes:
        if n.level == 1:
            immediate = [c for c in nodes if c.parent_idx == n.idx]
            if len(immediate) < args.min_subsections:
                warnings.append(
                    f"Top-level section `{n.title}` (line {n.line_no}) has {len(immediate)} subsection(s), below min {args.min_subsections}."
                )

    for parent, siblings in by_parent.items():
        for i in range(len(siblings)):
            for j in range(i + 1, len(siblings)):
                a = siblings[i]
                b = siblings[j]
                if is_similar(a.title, b.title, args.overlap_threshold):
                    warnings.append(
                        f"Potential sibling overlap under parent `{parent}`: line {a.line_no} `{a.title}` vs line {b.line_no} `{b.title}`."
                    )

    output = [
        "# Outline Lint Report",
        "",
        f"- Input: `{outline_path}`",
        f"- Heading count: {len(nodes)}",
        f"- Errors: {len(errors)}",
        f"- Warnings: {len(warnings)}",
        "",
    ]

    if errors:
        output.append("## Errors")
        output.append("")
        output.extend(f"- {msg}" for msg in errors)
        output.append("")
    if warnings:
        output.append("## Warnings")
        output.append("")
        output.extend(f"- {msg}" for msg in warnings)
        output.append("")
    if not errors and not warnings:
        output.append("No issues found.")
        output.append("")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(output), encoding="utf-8")
    print(f"Wrote outline lint report: {report_path}")

    if errors:
        return 2
    if warnings and args.fail_on_warning:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
