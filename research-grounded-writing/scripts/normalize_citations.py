#!/usr/bin/env python3
"""Convert source handles like [@source-id] into numeric citations [1], [2], ..."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HANDLE_RE = re.compile(r"\[@([A-Za-z0-9._:-]+)\]")


def normalize(text: str) -> tuple[str, dict[str, int]]:
    order: dict[str, int] = {}

    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in order:
            order[key] = len(order) + 1
        return f"[{order[key]}]"

    return HANDLE_RE.sub(repl, text), order


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize source-handle citations.")
    parser.add_argument("input", help="Input text file")
    parser.add_argument("--output", help="Output text file; defaults to stdout")
    parser.add_argument(
        "--map-output",
        help="Optional JSON file for citation mapping",
    )
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    normalized, mapping = normalize(text)

    if args.output:
        Path(args.output).write_text(normalized, encoding="utf-8")
    else:
        print(normalized)

    if args.map_output:
        Path(args.map_output).write_text(
            json.dumps(mapping, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
