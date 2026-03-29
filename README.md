# Research Skills for Codex

[README_zh / 中文说明](README_zh.md)

Lightweight, open-source research skills for Codex, designed for systematic literature review, survey planning, grounded drafting, and revision. 📎

## Overview

This repository packages a practical research-writing workflow into reusable Codex skills.

The suite is designed around a simple separation of concerns:

- skills hold workflow logic, artifact contracts, and review discipline
- scripts handle deterministic and repetitive tasks
- optional infrastructure remains optional rather than becoming a default dependency

The result is a skill suite that stays usable without requiring a paper warehouse, a custom reranker service, or a multi-agent runtime.

## What is included

- `research-survey-workflow`
  - End-to-end workflow for systematic review, corpus building, outlining, drafting, and revision.
- `research-literature-curation`
  - Multi-perspective literature collection, screening, paper-folder organization, and evidence mapping.
- `research-outline-synthesis`
  - Rough outline generation, clustering, subsection expansion, and final cleanup.
- `research-grounded-writing`
  - Section-level drafting tied to sources, evidence maps, full-text notes, and section packets.
- `research-review-and-revise`
  - Corpus adequacy, coverage, structure, citation, and revision checks.
- `research-latex-export`
  - Export Markdown-first research artifacts into `.tex`, `.bib`, and optional `.pdf`.

## Workflow At A Glance

The full workflow is organized as:

1. Scope the topic and deliverable
2. Declare source mode (`manual-gated` for CNKI-like access, `api-automated` for arXiv-like access)
3. Stage A retrieval: read existing surveys and benchmark overviews first
4. Stage B retrieval: run topic/keyword search and build candidate pools
5. Build a candidate corpus and apply threshold-aware screening
6. Create full-text paper notes and run notes-quality validation (template placeholders do not count)
7. Add a lightweight full-text retrieval layer over the local paper corpus
8. Build a multi-level outline from clustered notes
9. Run outline lint and initialize subsection evidence packets
10. Draft grounded subsection prose into `subsection_drafts/` first, then merge into report drafts
11. Run conformance and citation-whitelist checks, then review for corpus adequacy, coverage, grounding, and structure
12. Revise with diff tracing and numeric quality gate ✍️
13. Optionally export the final draft into LaTeX and PDF

Each stage is also available as a standalone skill.

## Why this structure

This repository does **not** attempt to recreate a full research-agent runtime.

Instead, it keeps the architecture modular:

- skills: reasoning workflow, artifact contracts, review discipline
- scripts: search, metadata collection, local corpus retrieval, citation normalization, reference rendering
- optional infrastructure: local paper stores, rerankers, large indexes

## Recommended usage

Install all six skills together for the complete workflow.

Install individual skills when only one stage is needed:

- only source collection: `research-literature-curation`
- only outline generation: `research-outline-synthesis`
- only drafting: `research-grounded-writing`
- only review and revision: `research-review-and-revise`
- only LaTeX export: `research-latex-export`

## Installation

Copy one or more skill folders into your Codex skills directory:

- `$CODEX_HOME/skills`
- or `~/.codex/skills` if `CODEX_HOME` is unset

Example layout after installation:

```text
$CODEX_HOME/skills/
  research-survey-workflow/
  research-literature-curation/
  research-outline-synthesis/
  research-grounded-writing/
  research-review-and-revise/
  research-latex-export/
```

Each skill only requires a `SKILL.md` file to function. This repository also includes optional scripts and references.

## Platform support

- Tested on Windows 11.
- Linux and macOS compatibility has not been validated yet and may require path or command adaptations.

## Outputs By Phase

### Phase 1: Scope and bootstrap

- `topic_scope.md`
- `research_questions.md`
- `source_mode_decision.md`
- `acquisition_plan.md`
- `survey_query_pack.yaml`
- `topic_query_pack.yaml`
- `human_task_sheet.md` (for `manual-gated` source mode)
- `existing_surveys.md`

### Phase 2: Corpus building

- `candidate_pool.json`
- `screening_decisions.md`
- `source_inventory.json` or `source_inventory.md`
- `papers/<paper-id>/metadata.md`
- `papers/<paper-id>/notes.md`
- `papers/<paper-id>/bib.txt`
- `papers/<paper-id>/links.txt`

### Phase 3: Evidence and structure

- `evidence_map.json` or `evidence_map.md`
- `rough_outlines.md`
- `merged_outline.md`
- `subsection_outline.md`
- `draft_outline.md`
- `refined_outline.md`
- `outline_lint_report.md`
- `section_evidence_index.md`
- `corpus_queries/<query-id>.md`

### Phase 4: Writing and revision

- `section_packets/<section-id>.md`
- `subsection_drafts/<section-id>.md`
- `draft_report_raw.md`
- `draft_report_refined.md`
- `draft_report.md`
- `detailed_report.md`
- `coherence_edits.md`
- `citation_whitelist_report.md`
- `outline_conformance_report.md`
- `review_notes.md`
- `revision_delta.md`
- `revised_report.md`
- `quality_gate.json`

### Phase 5: Publication export

- `latex/main.tex`
- `latex/references.bib`
- `latex/build.log`
- `latex/compile_error.json`
- `latex/citation_gaps.md`
- `latex/paragraph_citation_gaps.md`
- `latex/main.pdf`

### Run metadata

- `run_manifest.json`
- `state_manifest.json`
- `artifact_validation_report.md`

These names are suggestions, not hard requirements.

## Design principles

This skill suite follows three defaults:

1. Prefer a simple workflow over a large runtime.
2. Prefer a small script over a heavy service.
3. Keep human review as an explicit checkpoint.

Failure-handling rule:

- If a required step cannot be satisfied (for example unreadable full text, failed CAJ/PDF decoding, or unresolved citation anchors), report the blocker first and do not silently continue as if the step succeeded.

Accordingly, the core workflow works without:

- a local paper vector database
- a cross-encoder reranker service
- a custom training pipeline
- a multi-agent orchestration runtime

## Corpus heuristics

For a substantial survey, a useful rule of thumb is:

- initial candidate pool: `80-150`
- title and abstract screened set: `40-60`
- full-text reading notes: `30-40+`

These are practical workflow targets, not publication rules. If the topic is unusually narrow, record the reason for a smaller corpus.
When source access is human-gated (for example CNKI), treat these numbers as recommendations only.

Threshold-aware screening and citation floor:

- if total collected records are `<15`, skip screening, include all, and prompt supplementation to at least `15`
- if total collected records are `15-29`, skip screening and include all records
- if total collected records are `>=30`, screening can be applied
- if total collected records are `<30`, cite all included sources in the body text
- if total collected records are `>=30` and screening is used, keep final body-text citations at `>=30` unique sources

## Outline heuristics

For a substantial survey:

- a refined outline should usually be multi-level, not a flat section list
- if the corpus has `20+` full-text notes, the refined outline should usually include at least `1.1` subsections and often `1.1.1` where useful
- subsection boundaries should come from clustered reading notes and evidence maps, not only from a generic template
- each subsection should have a distinct comparison purpose or evidence cluster

## Writing heuristics

For a detailed survey report:

- create a `section_packets/<section-id>.md` file before drafting important subsections
- draft full subsection prose in `subsection_drafts/<section-id>.md` before global merge
- retrieve evidence from both `notes.md` and the local full-text corpus under `papers/<paper-id>/src/`
- leave reusable retrieval traces in `corpus_queries/<query-id>.md` when the search materially shapes a subsection
- run one bounded supplemental retrieval pass for thin subsections instead of leaving placeholder prose
- for analytical subsections, keep at least `2` paragraphs and at least `3` sentences per paragraph (recommended `5+`)
- for analytical subsections, keep at least `2` unique citations (recommended `3+` for core argument subsections)
- include explicit caveat or boundary-condition discussion, not only positive claims

## Included scripts

- `research-literature-curation/scripts/search_arxiv.py`
  - Simple arXiv search helper.
- `research-literature-curation/scripts/export_arxiv_candidates.ps1`
  - Export a deduplicated arXiv candidate pool from multiple search queries on Windows.
- `research-literature-curation/scripts/materialize_paper_folders.ps1`
  - Build paper folders with metadata, notes, BibTeX, and links from a selected candidate set.
- `research-literature-curation/scripts/fetch_arxiv_sources.ps1`
  - Download and extract arXiv source packages into each paper folder.
- `research-literature-curation/scripts/search_corpus.ps1`
  - Search concept mentions across `notes.md`, `metadata.md`, and local full-text source files in `papers/`.
- `research-literature-curation/scripts/validate_notes_quality.py`
  - Validate that `papers/<paper-id>/notes.md` is substantive (not placeholders) and includes required sections/snippets.
- `research-grounded-writing/scripts/normalize_citations.py`
  - Convert source handles like `[@source-id]` into numeric citations.
- `research-grounded-writing/scripts/render_references.py`
  - Render a Markdown references section from a JSON file.
- `research-outline-synthesis/scripts/lint_outline.py`
  - Lint refined outlines for duplicate headings, empty sections, and overlap risks.
- `research-grounded-writing/scripts/init_section_packets.py`
  - Initialize packet skeletons from `refined_outline.md` with retrieval budgets.
- `research-grounded-writing/scripts/check_outline_conformance.py`
  - Check heading-id conformance between outline and report.
- `research-grounded-writing/scripts/check_citation_whitelist.py`
  - Enforce subsection-level citation whitelists from packet evidence.
- `research-grounded-writing/scripts/validate_section_packets.py`
  - Validate packet-set completeness against refined outline, detect placeholders, and optionally enforce language lock (`zh`/`en`).
- `research-grounded-writing/scripts/validate_subsection_drafts.py`
  - Validate subsection prose depth (`paragraph/sentence minimums`), citation density, and self-check completeness.
- `research-review-and-revise/scripts/quality_gate_scorecard.py`
  - Produce numeric quality gates (`coverage`, `structure`, `relevance`, citation precision/recall).
- `research-survey-workflow/scripts/validate_artifacts.py`
  - Validate phase artifacts and emit `state_manifest.json` for resumability.
- `research-latex-export/scripts/export_markdown_to_latex.py`
  - Convert a Markdown research report into a LaTeX manuscript.
- `research-latex-export/scripts/collect_bibtex.py`
  - Merge BibTeX entries from paper folders into `references.bib`.
- `research-latex-export/scripts/compile_latex_project.py`
  - Compile a generated LaTeX project with `latexmk` or `pdflatex`, and emit `compile_error.json`.
- `research-latex-export/scripts/audit_paragraph_citations.py`
  - Flag long LaTeX paragraphs that do not include any citation command.

These scripts are intentionally small and replaceable.

## Practical lessons

- Do not treat auto-generated packet templates as finished artifacts; validate and fill them before drafting.
- Packet coverage should match the required outline depth, otherwise section-level grounding will be uneven.
- For Chinese deliverables, keep packet explanatory fields primarily in Chinese to avoid language drift during drafting.

## Repository layout

```text
research-skills/
  README.md
  README_zh.md
  research-survey-workflow/
  research-literature-curation/
  research-outline-synthesis/
  research-grounded-writing/
  research-review-and-revise/
  research-latex-export/
```

## Minimal example

One practical usage pattern is:

1. Run `research-literature-curation` to read existing surveys, collect a candidate pool, build paper folders, and create an evidence map.
2. Use `search_corpus.ps1` to retrieve concept mentions from the local paper corpus when a subsection needs stronger grounding.
3. Run `research-outline-synthesis` to cluster notes into a multi-level outline.
4. Create subsection evidence packets such as `section_packets/5.1.1.md`.
5. Run `research-grounded-writing` to draft section-level text with explicit source handles.
6. Run `research-review-and-revise` to identify unsupported claims, corpus weaknesses, structural overlap, and coverage gaps.
7. Use the citation scripts to normalize citations and render a references section if needed.
8. Run `research-latex-export` to generate `latex/main.tex`, `latex/references.bib`, and optionally `latex/main.pdf`.

## Acknowledgements

This skill suite was informed by ideas from the following open-source projects:

- [STORM](https://github.com/stanford-oval/storm)
- [OpenScholar](https://github.com/AkariAsai/OpenScholar)
- [AutoSurvey](https://github.com/AutoSurveys/AutoSurvey)
- [Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory)

The goal here is not to repackage those projects, but to distill reusable workflow ideas for Codex skills.

## License

[MIT](LICENSE)
