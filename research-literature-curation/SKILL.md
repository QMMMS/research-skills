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
2. Decide source mode before retrieval:
   - `manual-gated`: CNKI-like sources requiring human browser operations
   - `api-automated`: arXiv-like sources suitable for scripted retrieval
3. Stage A (survey-first): search existing surveys/reviews/tutorials to build a baseline map.
4. Generate `3-6` perspectives or research angles from Stage A reading.
5. For each perspective, write a small set of Stage B topic queries.
6. Stage B (topic-keyword): search and collect topic-specific candidate papers.
7. Build candidate pools and triage the papers into:
   - must-read
   - useful background
   - probably out-of-scope
8. Screen titles and abstracts down to a working set.
9. Read full text for the core set and produce analytical notes per paper (not template placeholders).
10. Run notes quality validation before drafting.
11. Build a lightweight local corpus retrieval surface over the paper folders.
12. Extract evidence into a structured inventory.
13. Build an evidence map that can be reused by later writing stages.

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
- `src/fulltext.auto.pdf` (if extracted PDF exists)
- `src/fulltext.auto.txt` (if extracted TXT exists)

Artifact placement rule:

- extracted full-text artifacts must be copied into the corresponding `papers/<paper-id>/src/` folder
- do not keep `auto_pdf/auto_txt` as the only retrieval location once paper folders are built
- if an extracted artifact cannot be mapped to a `paper-id`, record it in a sync report (for example `acq/reports/paper_artifact_sync_report.json`) and mark the paper as partially linked

Reading completion rule:

- Placeholder bullets (`-`, `TODO`, `TBD`, `待补`) do not count as notes.
- A valid deep-read note must include concrete claims, method/argument understanding, evidence usage comments, and caveats.
- Add a short evidence-snippet block from full text to support your own interpretation.

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
- `scripts/validate_notes_quality.py`

Use it to gather subsection-level evidence before drafting or revising.

## Human-in-the-loop retrieval rules

When source mode is `manual-gated` (for example CNKI):

- explicitly tell the user which steps must be performed manually
- do not attempt login/captcha/slider bypass automation
- provide a compact human task sheet with:
  - query list
  - recommended retrieval volume
  - accepted download formats
  - citation export format priority

Recommended retrieval volumes (not mandatory):

- Stage A surveys: usually `8-20`
- Stage B topic papers: usually `30-100` candidate records before screening

If constraints (time/access) prevent these ranges, record rationale and continue.

If full-text acquisition or decoding fails for included papers:

- stop and report the blocker immediately
- record blocked items and impact in `reading_blockers.md`
- do not pretend full-text reading is complete

## Screening threshold rule

- If total collected records `<15`, skip screening, include all records, and prompt the user to supplement to at least `15`.
- If total collected records are `15-29`, skip screening and include all records.
- If total collected records `>=30`, screening can be applied.
- Citation policy:
- When total collected records are `<30`, cite all included sources in the body text.
- When total collected records are `>=30` and screening is used, keep final body-text citations at `>=30` unique sources.

## Keyword and download format conventions

For manual retrieval packs, define:

- `core_terms` (2-4)
- `expand_terms` (3-8)
- `exclude_terms` (0-4)
- `field` (`主题`, `关键词`, `篇名`, `作者`, etc.)
- `year_range`

Preferred full-text formats:

- `PDF` first
- `CAJ` allowed as fallback

Citation export preference:

- `BibTeX` first
- `RIS` or EndNote-compatible text as fallback

Use templates:

- `references/source_mode_decision_template.md`
- `references/manual_search_task_sheet_template.md`

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

## Optional sub-agent reading mode

When the corpus is large, you may parallelize full-text reading with sub-agents.

- split papers into disjoint ownership sets
- require each sub-agent to edit only its assigned `papers/<paper-id>/notes.md`
- run a primary-agent audit pass after merge for consistency and unsupported claims
- if any sub-agent reports unreadable text, escalate to user immediately instead of silently proceeding

## Scripts

If a simple arXiv search is enough, use:

- `scripts/search_arxiv.py`
- `scripts/export_arxiv_candidates.ps1`
- `scripts/search_corpus.ps1`

Do not build a local paper database unless the user explicitly wants that engineering overhead.
