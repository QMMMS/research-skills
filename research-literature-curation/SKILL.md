---
name: research-literature-curation
description: Multi-perspective literature collection, source screening, paper-folder organization, and evidence mapping for research tasks. Use when Codex needs source discovery, source triage, structured reading notes, or literature-review preparation.
---

# Research Literature Curation

Use this skill when the task is primarily about gathering, screening, and structuring sources.

Typical triggers:

- "collect papers on X"
- "help me survey this topic"
- "find the main research threads"
- "build a reading list"
- "organize evidence before writing"

## Core method

1. Define topic boundaries.
2. Search for existing surveys or review papers before expanding the corpus.
3. Generate `3-6` perspectives or research angles.
4. For each perspective, write a small set of search questions.
5. Search and collect candidate papers from primary sources.
6. Build an initial candidate pool, usually `80-150` papers for a formal survey.
7. Triage the papers into:
   - must-read
   - useful background
   - probably out-of-scope
8. Screen titles and abstracts down to a working set, usually `40-60`.
9. Produce structured notes for a core full-text set, usually `30-40+`.
10. Build a lightweight local corpus retrieval surface over the paper folders.
11. Extract evidence into a structured inventory.
12. Build an evidence map that can be reused by later writing stages.

## Perspective generation

Avoid roleplay. Do not simulate fake experts unless that meaningfully improves the task.

Instead, explicitly generate research perspectives such as:

- taxonomy
- methodology
- datasets or benchmarks
- evaluation criteria
- limitations
- applications
- open problems

## Source inventory

For each retained source, capture at least:

- stable source id
- title
- year
- venue or arXiv id if available
- abstract or short summary
- tags
- PDF link if available
- BibTeX or equivalent citation block
- why it matters
- what claims or sections it supports

Use the template in:

- `references/source_inventory_template.md`
- `references/source_policy_template.md`

For papers selected for deep reading, create one folder per paper and store:

- `metadata.md`
- `notes.md`
- `bib.txt`
- `links.txt`

Read:

- `references/corpus_layout.md`
- `references/paper_note_template.md`
- `references/screening_checklist.md`

Once paper folders exist, do not rely on `notes.md` alone for later writing.

Use the local corpus as a searchable evidence layer:

- search `notes.md` and `metadata.md`
- search full-text source files under `src/`
- search `bib.txt` and `links.txt` when citation recovery is helpful

Prefer the lightweight search script in:

- `scripts/search_corpus.ps1`

Use it to gather subsection-level evidence before drafting or revising.

## Evidence mapping

Build `evidence_map.json` or equivalent notes that connect:

- section or question
- relevant sources
- key claims
- caveats

This skill should prepare later drafting, not only collect URLs.

For reusable retrieval traces, prefer a stable per-query schema in `corpus_queries/<query-id>.md`:

- retrieval_query
- section_id or target_subsection
- doc_id / paper_id
- rank_before / rank_after (if rerank used)
- score
- support_span
- used_in_claims

Keep external retrieval controlled:

- trigger only when critique flags a concrete evidence gap
- deduplicate against local inventory before accepting new sources
- mark each source with reliability tier from source policy

## Scripts

If a simple arXiv search is enough, use:

- `scripts/search_arxiv.py`
- `scripts/export_arxiv_candidates.ps1`
- `scripts/search_corpus.ps1`

Do not build a local paper database unless the user explicitly wants that engineering overhead.
