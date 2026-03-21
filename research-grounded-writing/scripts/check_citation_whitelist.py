from __future__ import annotations

import argparse
import re
from pathlib import Path


MD_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
NUMBERED_PREFIX_RE = re.compile(r"^((?:\d+\.)*\d+)\s+(.+?)\s*$")
MD_CITE_RE = re.compile(r"\[@([^\]]+)\]")
LATEX_CITE_RE = re.compile(r"\\cite[tpauthoralt]*\{([^}]+)\}")
ID_TOKEN_RE = re.compile(r"[A-Za-z0-9_.:\-]+")


def parse_citation_keys(text: str) -> set[str]:
    keys: set[str] = set()
    for m in MD_CITE_RE.finditer(text):
        parts = re.split(r"[;,]", m.group(1))
        for p in parts:
            key = p.strip().lstrip("@")
            if key:
                keys.add(key)
    for m in LATEX_CITE_RE.finditer(text):
        parts = re.split(r"[;,]", m.group(1))
        for p in parts:
            key = p.strip()
            if key:
                keys.add(key)
    return keys


def parse_packet_whitelist(packet_path: Path) -> set[str]:
    text = packet_path.read_text(encoding="utf-8", errors="ignore")
    keys = parse_citation_keys(text)

    capture = False
    for raw in text.splitlines():
        line = raw.rstrip()
        if MD_HEADING_RE.match(line):
            title = MD_HEADING_RE.match(line).group(2).strip().lower()
            capture = "relevant source id" in title or "relevant sources" in title
            continue
        if not capture:
            continue
        if not line.strip().startswith("-"):
            continue
        payload = line.strip().lstrip("-").strip().strip("`")
        for token in ID_TOKEN_RE.findall(payload):
            if token and not token.isdigit():
                keys.add(token)
    return keys


def parse_report_subsection_citations(report_path: Path) -> dict[str, set[str]]:
    text = report_path.read_text(encoding="utf-8", errors="ignore")
    citations_by_section: dict[str, set[str]] = {}
    current_sid: str | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer, current_sid
        if current_sid is None:
            buffer = []
            return
        citations = parse_citation_keys("\n".join(buffer))
        citations_by_section.setdefault(current_sid, set()).update(citations)
        buffer = []

    for raw in text.splitlines():
        line = raw.rstrip()
        md = MD_HEADING_RE.match(line)
        candidate = md.group(2).strip() if md else line.strip()
        n = NUMBERED_PREFIX_RE.match(candidate)
        if md and n:
            flush()
            current_sid = n.group(1).strip()
            continue
        if current_sid is not None:
            buffer.append(line)
    flush()
    return citations_by_section


def main() -> int:
    parser = argparse.ArgumentParser(description="Check section-level citation whitelist against section packets.")
    parser.add_argument("--packets-dir", required=True, help="Directory containing section packet markdown files")
    parser.add_argument("--report", required=True, help="Draft/revised report markdown file")
    parser.add_argument("--output", required=True, help="Output report markdown path")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if whitelist violations exist")
    args = parser.parse_args()

    packets_dir = Path(args.packets_dir).resolve()
    report_path = Path(args.report).resolve()
    output_path = Path(args.output).resolve()

    whitelist_by_section: dict[str, set[str]] = {}
    for p in sorted(packets_dir.glob("*.md")):
        if p.name.startswith("_"):
            continue
        sid = p.stem
        whitelist_by_section[sid] = parse_packet_whitelist(p)

    citations_by_section = parse_report_subsection_citations(report_path)

    violations: list[str] = []
    warnings: list[str] = []
    for sid, citations in sorted(citations_by_section.items()):
        allowed = whitelist_by_section.get(sid)
        if allowed is None:
            if citations:
                warnings.append(f"`{sid}` has citations but no corresponding packet whitelist file.")
            continue
        disallowed = sorted(citations - allowed)
        if disallowed:
            violations.append(f"`{sid}` disallowed citations: {', '.join(disallowed)}")

    lines = [
        "# Citation Whitelist Report",
        "",
        f"- Packets dir: `{packets_dir}`",
        f"- Report: `{report_path}`",
        f"- Packet whitelist sections: {len(whitelist_by_section)}",
        f"- Report cited sections: {len(citations_by_section)}",
        f"- Violations: {len(violations)}",
        f"- Warnings: {len(warnings)}",
        "",
    ]

    if violations:
        lines.append("## Violations")
        lines.append("")
        lines.extend(f"- {v}" for v in violations)
        lines.append("")
    if warnings:
        lines.append("## Warnings")
        lines.append("")
        lines.extend(f"- {w}" for w in warnings)
        lines.append("")
    if not violations and not warnings:
        lines.append("No whitelist issues found.")
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote whitelist report: {output_path}")

    if args.strict and violations:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
