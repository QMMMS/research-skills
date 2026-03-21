from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


MD_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
NUMBERED_PREFIX_RE = re.compile(r"^((?:\d+\.)*\d+)\s+(.+?)\s*$")


@dataclass
class OutlineNode:
    level: int
    section_id: str
    title: str


def parse_outline_nodes(markdown: str) -> list[OutlineNode]:
    nodes: list[OutlineNode] = []
    for raw in markdown.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue

        md = MD_HEADING_RE.match(line)
        if md:
            level = len(md.group(1))
            text = md.group(2).strip()
        else:
            level = 0
            text = line.strip()

        match = NUMBERED_PREFIX_RE.match(text)
        if not match:
            continue
        section_id = match.group(1).strip()
        title = match.group(2).strip()
        inferred = section_id.count(".") + 1
        level = max(level, inferred)
        nodes.append(OutlineNode(level=level, section_id=section_id, title=title))
    return nodes


def packet_template(
    section_id: str,
    title: str,
    top_k: int,
    min_unique_sources: int,
    max_sibling_overlap: float,
) -> str:
    return (
        f"# Section Packet {section_id}\n\n"
        f"## Subsection Title\n\n"
        f"{title}\n\n"
        "## Section Goal\n\n"
        "- Fill in a concrete objective for this subsection.\n\n"
        "## Retrieval Budget\n\n"
        f"- top_k_per_query: {top_k}\n"
        f"- min_unique_sources: {min_unique_sources}\n"
        f"- max_sibling_source_overlap_ratio: {max_sibling_overlap:.2f}\n"
        "- retrieval_queries:\n"
        "  - <query-1>\n"
        "  - <query-2>\n\n"
        "## Relevant Notes\n\n"
        "- papers/<paper-id>/notes.md#<anchor or line>\n\n"
        "## Relevant Source IDs\n\n"
        "- <source-id-1>\n"
        "- <source-id-2>\n\n"
        "## Key Claims\n\n"
        "- claim: <claim text>\n"
        "  support: [@<source-id-1>]\n\n"
        "## Caveats\n\n"
        "- unresolved conflict or limitation\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize section packet files from a refined outline.")
    parser.add_argument("--outline", required=True, help="Path to refined_outline.md")
    parser.add_argument("--output-dir", required=True, help="Directory to place section packet files")
    parser.add_argument("--min-level", type=int, default=2, help="Only create packets for headings at or deeper than this level")
    parser.add_argument("--top-k", type=int, default=12, help="Default top-k retrieval budget per query")
    parser.add_argument("--min-unique-sources", type=int, default=4, help="Default minimum unique source count per packet")
    parser.add_argument(
        "--max-sibling-overlap",
        type=float,
        default=0.60,
        help="Default maximum sibling source overlap ratio",
    )
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing packet files")
    args = parser.parse_args()

    outline_path = Path(args.outline).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    nodes = parse_outline_nodes(outline_path.read_text(encoding="utf-8", errors="ignore"))
    targets = [n for n in nodes if n.level >= args.min_level]

    created: list[Path] = []
    skipped: list[Path] = []
    for node in targets:
        packet_path = output_dir / f"{node.section_id}.md"
        if packet_path.exists() and not args.overwrite:
            skipped.append(packet_path)
            continue
        packet_path.write_text(
            packet_template(
                section_id=node.section_id,
                title=node.title,
                top_k=args.top_k,
                min_unique_sources=args.min_unique_sources,
                max_sibling_overlap=args.max_sibling_overlap,
            ),
            encoding="utf-8",
        )
        created.append(packet_path)

    index_lines = [
        "# Section Packet Index",
        "",
        f"- Outline: `{outline_path}`",
        f"- Output dir: `{output_dir}`",
        f"- Created: {len(created)}",
        f"- Skipped existing: {len(skipped)}",
        "",
        "## Packet files",
        "",
    ]
    for p in sorted(created + skipped):
        status = "created" if p in created else "existing"
        index_lines.append(f"- `{p.name}` ({status})")
    (output_dir / "_index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    print(f"Created {len(created)} packet(s), skipped {len(skipped)} existing packet(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
