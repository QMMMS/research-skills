from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a numeric quality gate scorecard for a research draft.")
    parser.add_argument("--output", required=True, help="Path to write quality_gate.json")
    parser.add_argument("--coverage", type=float, required=True, help="Coverage score, usually 1-5")
    parser.add_argument("--structure", type=float, required=True, help="Structure score, usually 1-5")
    parser.add_argument("--relevance", type=float, required=True, help="Relevance score, usually 1-5")
    parser.add_argument("--citation-precision", type=float, required=True, help="Citation precision in [0,1]")
    parser.add_argument("--citation-recall", type=float, default=-1.0, help="Citation recall in [0,1], optional")
    parser.add_argument("--min-coverage", type=float, default=3.0)
    parser.add_argument("--min-structure", type=float, default=3.0)
    parser.add_argument("--min-relevance", type=float, default=3.0)
    parser.add_argument("--min-citation-precision", type=float, default=0.60)
    parser.add_argument("--min-citation-recall", type=float, default=0.50)
    args = parser.parse_args()

    checks = {
        "coverage": (args.coverage, args.min_coverage),
        "structure": (args.structure, args.min_structure),
        "relevance": (args.relevance, args.min_relevance),
        "citation_precision": (args.citation_precision, args.min_citation_precision),
    }
    if args.citation_recall >= 0:
        checks["citation_recall"] = (args.citation_recall, args.min_citation_recall)

    failed = [name for name, (value, threshold) in checks.items() if value < threshold]
    passed = len(failed) == 0

    payload = {
        "passed": passed,
        "scores": {
            "coverage": args.coverage,
            "structure": args.structure,
            "relevance": args.relevance,
            "citation_precision": args.citation_precision,
            "citation_recall": None if args.citation_recall < 0 else args.citation_recall,
        },
        "thresholds": {
            "coverage": args.min_coverage,
            "structure": args.min_structure,
            "relevance": args.min_relevance,
            "citation_precision": args.min_citation_precision,
            "citation_recall": None if args.citation_recall < 0 else args.min_citation_recall,
        },
        "failed_checks": failed,
    }

    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote quality gate scorecard to {output_path}")

    if not passed:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
