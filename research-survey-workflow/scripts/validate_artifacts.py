from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


PHASE_REQUIREMENTS = {
    "phase1": [["topic_scope.md"], ["research_questions.md"], ["existing_surveys.md"]],
    "phase2": [["candidate_pool.json", "candidate_pool.md"], ["screening_decisions.md"], ["source_inventory.json", "source_inventory.md"]],
    "phase3": [["evidence_map.json", "evidence_map.md"], ["draft_outline.md"], ["refined_outline.md"]],
    "phase4": [["draft_report.md"], ["detailed_report.md"], ["review_notes.md"], ["revised_report.md"]],
}


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate research workflow artifacts and emit a state manifest.")
    parser.add_argument("--run-root", required=True, help="Run directory containing workflow outputs")
    parser.add_argument("--report", required=True, help="Path to write markdown validation report")
    parser.add_argument(
        "--state-manifest",
        required=True,
        help="Path to write state_manifest.json",
    )
    args = parser.parse_args()

    run_root = Path(args.run_root).resolve()
    report_path = Path(args.report).resolve()
    manifest_path = Path(args.state_manifest).resolve()

    missing: dict[str, list[str]] = {}
    found: dict[str, list[str]] = {}
    file_hashes: dict[str, str] = {}

    for phase, req_groups in PHASE_REQUIREMENTS.items():
        miss: list[str] = []
        hit: list[str] = []
        for alternatives in req_groups:
            matched = None
            for rel in alternatives:
                p = run_root / rel
                if p.exists():
                    matched = rel
                    hit.append(rel)
                    file_hashes[rel] = file_sha256(p)
                    break
            if matched is None:
                miss.append(" | ".join(alternatives))
        if miss:
            missing[phase] = miss
        found[phase] = hit

    report_lines = [
        "# Artifact Validation Report",
        "",
        f"- Run root: `{run_root}`",
        f"- Missing phases: {len(missing)}",
        "",
    ]
    for phase in PHASE_REQUIREMENTS:
        report_lines.append(f"## {phase}")
        report_lines.append("")
        report_lines.append(f"- Found: {len(found.get(phase, []))}")
        if missing.get(phase):
            report_lines.append(f"- Missing: {len(missing[phase])}")
            for rel in missing[phase]:
                report_lines.append(f"  - `{rel}`")
        else:
            report_lines.append("- Missing: 0")
        report_lines.append("")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines), encoding="utf-8")

    manifest = {
        "run_root": str(run_root),
        "required_phases": list(PHASE_REQUIREMENTS.keys()),
        "found": found,
        "missing": missing,
        "file_hashes": file_hashes,
        "recoverable": len(missing) == 0,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Wrote artifact validation report: {report_path}")
    print(f"Wrote state manifest: {manifest_path}")
    if missing:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
