#!/usr/bin/env python3
"""Simple arXiv search helper for research skill workflows."""

from __future__ import annotations

import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Search arXiv and print compact results.")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--max-results", type=int, default=10, help="Maximum number of results")
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="Output format",
    )
    args = parser.parse_args()

    try:
        import arxiv  # type: ignore
    except ImportError:
        print(
            "Missing dependency: install the 'arxiv' package to use this script.",
            file=sys.stderr,
        )
        return 1

    client = arxiv.Client()
    search = arxiv.Search(
        query=args.query,
        max_results=args.max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    results = []
    for paper in client.results(search):
        results.append(
            {
                "title": paper.title,
                "summary": paper.summary,
                "published": str(paper.published.date()),
                "authors": [author.name for author in paper.authors],
                "pdf_url": paper.pdf_url,
                "entry_id": paper.entry_id,
            }
        )

    if args.format == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for idx, item in enumerate(results, start=1):
            print(f"{idx}. {item['title']}")
            print(f"   Published: {item['published']}")
            print(f"   URL: {item['entry_id']}")
            print(f"   PDF: {item['pdf_url']}")
            print(f"   Authors: {', '.join(item['authors'])}")
            print(f"   Summary: {item['summary']}")
            print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
