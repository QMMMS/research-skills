from __future__ import annotations

import argparse
import re
from pathlib import Path


ENTRY_RE = re.compile(r"@\w+\s*{\s*([^,]+),", re.MULTILINE)
EPRINT_RE = re.compile(r"\beprint\s*=\s*[{\"\s]*([^}\",\n]+)", re.IGNORECASE)
ARXIV_PREFIX_RE = re.compile(r"^arxiv\s*:\s*", re.IGNORECASE)
ARXIV_ID_RE = re.compile(r"^(\d{4})\.(\d{4,5})(v(\d+))?$", re.IGNORECASE)


def extract_entries(text: str) -> list[str]:
    entries: list[str] = []
    starts = [m.start() for m in re.finditer(r"@\w+\s*{", text)]
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(text)
        chunk = text[start:end].strip()
        if chunk:
            entries.append(chunk)
    return entries


def parse_eprint_id(entry: str) -> str | None:
    match = EPRINT_RE.search(entry)
    if not match:
        return None
    raw = match.group(1).strip()
    raw = ARXIV_PREFIX_RE.sub("", raw)
    return raw or None


def to_safe_arxiv_key(arxiv_id: str) -> str | None:
    match = ARXIV_ID_RE.match(arxiv_id)
    if not match:
        return None
    yymm = match.group(1)
    number = match.group(2)
    version = match.group(4)
    if version:
        return f"arxiv_{yymm}_{number}_v{version}"
    return f"arxiv_{yymm}_{number}"


def alias_candidates(key: str, eprint_id: str | None) -> list[str]:
    candidates: list[str] = []
    if eprint_id:
        if eprint_id != key:
            candidates.append(eprint_id)
        safe_full = to_safe_arxiv_key(eprint_id)
        if safe_full and safe_full != key:
            candidates.append(safe_full)
        # Add version-less alias for citations using arXiv ID without vN suffix.
        base = re.sub(r"v\d+$", "", eprint_id)
        if base and base != eprint_id and base != key:
            candidates.append(base)
            safe_base = to_safe_arxiv_key(base)
            if safe_base and safe_base != key:
                candidates.append(safe_base)
    return candidates


def replace_entry_key(entry: str, new_key: str) -> str:
    return ENTRY_RE.sub(lambda m: m.group(0).replace(m.group(1), new_key, 1), entry, count=1)


def collect_entries(papers_root: Path) -> list[str]:
    dedup: dict[str, str] = {}
    for bib_file in sorted(papers_root.glob("*/bib.txt")):
        text = bib_file.read_text(encoding="utf-8", errors="ignore")
        for entry in extract_entries(text):
            match = ENTRY_RE.search(entry)
            if not match:
                continue
            key = match.group(1).strip()
            dedup.setdefault(key, entry)
            eprint_id = parse_eprint_id(entry)
            for alias in alias_candidates(key, eprint_id):
                if alias not in dedup:
                    dedup[alias] = replace_entry_key(entry, alias)
    return list(dedup.values())


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect BibTeX entries from paper folders.")
    parser.add_argument("--papers-root", required=True, help="Path to papers/<paper-id>/... root")
    parser.add_argument("--output", required=True, help="Output .bib path")
    args = parser.parse_args()

    papers_root = Path(args.papers_root)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    entries = collect_entries(papers_root)
    text = "\n\n".join(entries).strip() + ("\n" if entries else "")
    output.write_text(text, encoding="utf-8")

    print(f"Collected {len(entries)} BibTeX entries into {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
