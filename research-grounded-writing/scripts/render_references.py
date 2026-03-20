#!/usr/bin/env python3
"""Render a simple Markdown references list from JSON metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def format_entry(item: dict) -> str:
    title = item.get("title", "Untitled")
    authors = item.get("authors", [])
    year = item.get("year", "n.d.")
    venue = item.get("venue", "")
    url = item.get("url", "")

    authors_str = ", ".join(authors) if authors else "Unknown authors"
    core = f"{authors_str} ({year}). {title}."
    if venue:
        core += f" {venue}."
    if url:
        core += f" {url}"
    return core


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Markdown references from JSON.")
    parser.add_argument("input", help="JSON file with a list of reference entries")
    parser.add_argument("--output", help="Output Markdown file; defaults to stdout")
    args = parser.parse_args()

    items = json.loads(Path(args.input).read_text(encoding="utf-8"))
    lines = ["## References", ""]
    for idx, item in enumerate(items, start=1):
        lines.append(f"{idx}. {format_entry(item)}")

    text = "\n".join(lines) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
