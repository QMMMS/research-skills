from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
CITATION_RE = re.compile(r"\[@([^\]]+)\]")
SENTENCE_RE = re.compile(r"[。！？!?\.]+")


@dataclass
class DraftCheck:
    file: str
    ok: bool
    issues: list[str]
    paragraph_count: int
    min_sentences_found: int
    unique_citations: int


def extract_section(text: str, heading: str) -> str:
    lines = text.splitlines()
    in_section = False
    buf: list[str] = []
    for line in lines:
        m = HEADING_RE.match(line.strip())
        if m:
            name = m.group(1).strip()
            if in_section:
                break
            if name == heading:
                in_section = True
            continue
        if in_section:
            buf.append(line)
    return "\n".join(buf).strip()


def split_paragraphs(text: str) -> list[str]:
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    # remove single-line list bullets in case template placeholders remain
    cleaned: list[str] = []
    for p in paras:
        if all(line.strip().startswith("- ") for line in p.splitlines() if line.strip()):
            continue
        cleaned.append(p)
    return cleaned


def sentence_count(paragraph: str) -> int:
    return len([m for m in SENTENCE_RE.findall(paragraph)])


def check_file(path: Path, min_paragraphs: int, min_sentences: int, min_citations: int) -> DraftCheck:
    text = path.read_text(encoding="utf-8", errors="replace")
    issues: list[str] = []

    grounded = extract_section(text, "Grounded Draft")
    if not grounded:
        issues.append("missing or empty section: Grounded Draft")
        return DraftCheck(
            file=str(path),
            ok=False,
            issues=issues,
            paragraph_count=0,
            min_sentences_found=0,
            unique_citations=0,
        )

    paragraphs = split_paragraphs(grounded)
    if len(paragraphs) < min_paragraphs:
        issues.append(f"Grounded Draft has {len(paragraphs)} paragraphs (< {min_paragraphs})")

    sentence_counts = [sentence_count(p) for p in paragraphs] if paragraphs else [0]
    min_found = min(sentence_counts) if sentence_counts else 0
    for idx, cnt in enumerate(sentence_counts, start=1):
        if cnt < min_sentences:
            issues.append(f"paragraph {idx} has {cnt} sentences (< {min_sentences})")

    unique_cites = len(set(CITATION_RE.findall(grounded)))
    if unique_cites < min_citations:
        issues.append(f"unique citations in Grounded Draft: {unique_cites} (< {min_citations})")

    self_check = extract_section(text, "Self-check")
    if not self_check:
        issues.append("missing section: Self-check")
    else:
        if "needs_retrieval_reopen:" not in self_check:
            issues.append("Self-check missing field: needs_retrieval_reopen")
        if "evidence_coverage:" not in self_check:
            issues.append("Self-check missing field: evidence_coverage")
        if "overclaim_risk:" not in self_check:
            issues.append("Self-check missing field: overclaim_risk")

    return DraftCheck(
        file=str(path),
        ok=len(issues) == 0,
        issues=issues,
        paragraph_count=len(paragraphs),
        min_sentences_found=min_found,
        unique_citations=unique_cites,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate subsection draft completeness and prose depth.")
    parser.add_argument("--drafts-dir", required=True, help="Directory containing subsection_drafts/*.md")
    parser.add_argument("--report", required=True, help="Markdown report output path")
    parser.add_argument("--json-output", default="", help="Optional JSON report path")
    parser.add_argument("--min-paragraphs", type=int, default=2)
    parser.add_argument("--min-sentences", type=int, default=3)
    parser.add_argument("--min-citations", type=int, default=2)
    args = parser.parse_args()

    drafts_dir = Path(args.drafts_dir).resolve()
    report_path = Path(args.report).resolve()
    json_path = Path(args.json_output).resolve() if args.json_output else None

    files = sorted(drafts_dir.glob("*.md"))
    checks = [check_file(f, args.min_paragraphs, args.min_sentences, args.min_citations) for f in files]
    failed = [c for c in checks if not c.ok]
    passed = [c for c in checks if c.ok]

    lines = [
        "# Subsection Draft Validation Report",
        "",
        f"- drafts_dir: `{drafts_dir}`",
        f"- total: {len(checks)}",
        f"- passed: {len(passed)}",
        f"- failed: {len(failed)}",
        f"- min_paragraphs: {args.min_paragraphs}",
        f"- min_sentences: {args.min_sentences}",
        f"- min_citations: {args.min_citations}",
        "",
    ]

    if failed:
        lines += ["## Failed Drafts", ""]
        for item in failed:
            lines.append(f"### {Path(item.file).name}")
            lines.append(f"- paragraphs: {item.paragraph_count}")
            lines.append(f"- min_sentences_found: {item.min_sentences_found}")
            lines.append(f"- unique_citations: {item.unique_citations}")
            for issue in item.issues:
                lines.append(f"- issue: {issue}")
            lines.append("")
    else:
        lines += ["All subsection drafts passed validation.", ""]

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")

    if json_path is not None:
        payload = {
            "drafts_dir": str(drafts_dir),
            "total": len(checks),
            "passed": len(passed),
            "failed": len(failed),
            "checks": [
                {
                    "file": c.file,
                    "ok": c.ok,
                    "issues": c.issues,
                    "paragraph_count": c.paragraph_count,
                    "min_sentences_found": c.min_sentences_found,
                    "unique_citations": c.unique_citations,
                }
                for c in checks
            ],
        }
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Wrote subsection draft validation report: {report_path}")
    if json_path is not None:
        print(f"Wrote subsection draft validation json: {json_path}")
    return 0 if len(failed) == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
