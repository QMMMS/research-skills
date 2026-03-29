---
name: research-survey-workflow
description: End-to-end workflow for systematic literature review, survey planning, source-grounded drafting, and revision. Use when Codex needs a full research-writing pipeline with explicit source collection, screening, full-text reading notes, multi-level outlining, section-level retrieval, and revision rather than a single isolated step.
---

# Research Survey Workflow

Use this skill for end-to-end research writing tasks such as:

- literature reviews
- survey first drafts
- related work sections
- research landscape reports
- proposal background sections

Do not use this skill when the user clearly wants only one stage. In those cases prefer:

- `research-literature-curation`
- `research-outline-synthesis`
- `research-grounded-writing`
- `research-review-and-revise`

## Workflow

Run the task in this order unless the user explicitly wants a subset:

1. Clarify topic, scope, audience, and deliverable.
2. Declare source mode and human involvement before retrieval:
   - `manual-gated` (for CNKI-like sources with login/captcha/slider)
   - `api-automated` (for arXiv/OpenAlex/Crossref-like sources)
3. Create `topic_scope.md`, `research_questions.md`, and `source_mode_decision.md`.
4. Stage A retrieval: search existing surveys/tutorials/benchmark overviews and read them first.
5. Stage B retrieval: search topic-specific papers by keywords and expansions.
6. Build candidate pools and apply conditional screening.
7. Produce full-text reading notes for the core set.
8. Run a notes quality gate: template placeholders or empty bullets do not count as reading completion.
9. Organize corpus metadata, paper folders, and source inventory.
10. Add a lightweight local corpus retrieval layer over `papers/<paper-id>/...`.
11. Build an `evidence_map.json` or equivalent section-wise evidence notes.
12. Generate rough outlines from clustered notes.
13. Merge and expand into a refined multi-level outline.
14. For each section and subsection, create a `section_packets/<section-id>.md` evidence packet.
15. Validate packet completeness and placeholders before drafting (`validate_section_packets.py`).
16. Run a local evidence retrieval pass against notes, metadata, and full-text corpus files, and record the result in the packet.
17. Draft subsection-level prose into `subsection_drafts/<section-id>.md` grounded in packet evidence.
18. Run a bounded critique pass on each subsection, retrieve supplemental evidence where needed, update the packet, and revise subsection drafts.
19. Add a subsection stance pass: each analytical subsection must include one clear claim-first opening sentence.
20. Merge ready subsection drafts into report-level drafts (`draft_report*.md` / `detailed_report.md`).
21. Run structure/citation checks (`outline conformance`, `citation whitelist`) before full-draft merge.
22. Review the full draft for corpus adequacy, coverage, structure, citation support, overclaiming, and fence-sitting language.
23. Revise the draft and generate a revision delta.
24. Generate a numeric quality gate scorecard before publication export.
25. Optionally normalize citations and render a references section.
26. Optionally export the final draft into a LaTeX project and compile PDF with `research-latex-export`.

## Required habits

- Prefer explicit source-backed claims.
- Separate drafting from review.
- Keep intermediate artifacts on disk when the task is substantial.
- Keep a run-level manifest and phase-level state manifest for resumability and audit.
- Stop and surface major evidence gaps instead of hallucinating around them.
- If a required step cannot be satisfied (for example unreadable full text, failed OCR/CAJ decoding, missing citation anchors), stop and report the blocker to the user before continuing.
- Ask for human judgment only at meaningful checkpoints, not after every micro-step.
- Treat existing surveys as starting points, not as substitutes for reading primary papers.
- If source mode is `manual-gated`, do not automate login, captcha, slider, or anti-bot bypass.
- Do not describe a survey as substantial if it lacks an explicit corpus decision (`screened` or `include-all-under-threshold`) and full-text notes.
- Do not treat a one-level outline as a refined outline.
- Do not treat script-only note autofill as full-text reading completion; each included paper needs explicit analytical notes.
- For sub-agent collaboration, use small batches and verify process gates after each batch before issuing more assignments.
- Final report prose must not expose workflow internals (`本节主张`, `section packet`, `run step`, `agent step`) in abstract/body/conclusion.

Optional sub-agent reading mode:

- parallel reading is allowed when corpus size is large
- assign disjoint paper ownership to each sub-agent
- require each sub-agent to edit only assigned `papers/<paper-id>/notes.md`
- run a primary-agent consistency audit before drafting

## Outline expectations

For a substantial survey:

- the refined outline should usually include `1 / 1.1 / 1.1.1` style depth where appropriate
- subsections should emerge from clustered notes, not only from a generic survey template
- each major section should usually map to a distinct evidence cluster
- each subsection should have a visible drafting purpose, comparison axis, or evaluative role

## Writing expectations

For a detailed survey report:

- drafting should happen subsection by subsection
- each important subsection should usually have a `section_packets/<section-id>.md`
- each important subsection should usually have a paired `subsection_drafts/<section-id>.md`
- each subsection should trigger its own local corpus retrieval step
- each subsection should be checked for thinness before moving on
- weak subsections should receive one bounded supplementary retrieval pass rather than being left as placeholder prose
- section packet sets should be complete at required depth, not partial
- packet text language should follow target draft language for that run
- each analytical subsection should start with an explicit claim sentence and keep one dominant argument thread
- caveats should be written as scope/applicability constraints, not as fence-sitting conclusions
- helper tags may be used in intermediate drafts, but must be removed in publication-facing reports (`main_report.md`, `detailed_report.md`, `revised_report.md`)
- analytical subsection drafts should usually satisfy:
- `2+` paragraphs
- `3+` sentences per paragraph (recommended `5+`)
- `2+` unique citations (recommended `3+` for core subsections)
- explicit caveat or boundary-condition discussion

## Output contract

When running the full workflow, try to leave behind:

### Phase 1: Scope and bootstrap

- `topic_scope.md`
- `research_questions.md`
- `source_mode_decision.md`
- `acquisition_plan.md`
- `survey_query_pack.yaml`
- `topic_query_pack.yaml`
- `human_task_sheet.md` (when source mode is `manual-gated`)
- `existing_surveys.md`

### Phase 2: Corpus building

- `candidate_pool.json` or `candidate_pool.md`
- `screening_decisions.md`
- `source_inventory.json` or `source_inventory.md`
- `papers/<paper-id>/metadata.md`
- `papers/<paper-id>/notes.md`
- `papers/<paper-id>/bib.txt`
- `papers/<paper-id>/links.txt`
- `reading_blockers.md` (required when any included source lacks readable full text)

### Phase 3: Evidence and structure

- `evidence_map.json` or equivalent notes
- `rough_outlines.md`
- `merged_outline.md`
- `subsection_outline.md`
- `draft_outline.md`
- `refined_outline.md`
- `outline_lint_report.md`
- `section_evidence_index.md`
- `corpus_queries/<query-id>.md` when local corpus retrieval is material

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
- `latex/main.pdf`

### Run metadata

- `run_manifest.json`
- `state_manifest.json`
- `artifact_validation_report.md`

## Engineering defaults

Prefer lightweight operation by default:

- avoid local paper databases unless explicitly requested
- avoid heavy rerankers unless simple ranking is inadequate
- use small scripts for corpus retrieval and citation cleanup instead of large infrastructure

If the user wants a formal survey, prefer a traceable corpus layout over ad hoc notes.

## Corpus expectations

For a serious survey, suggested targets are:

- initial candidate pool: `80-150`
- title and abstract screened set: `40-60`
- full-text notes: `30-40+`

These are workflow heuristics, not hard publication rules. If the topic is unusually narrow, record the reason for a smaller corpus instead of pretending the literature is larger than it is.
If a human-gated source is time-limited, prioritize quality of coverage and rationale over forcing a numeric target.

## Screening and citation thresholds

- If total collected records `<15`, skip screening, include all records, and prompt supplementation to at least `15`.
- If total collected records are `15-29`, skip screening and include all records.
- If total collected records `>=30`, screening is allowed and should be documented.
- Citation policy:
- When total collected records are `<30`, cite all included sources in the body text.
- When total collected records are `>=30` and screening is used, keep final body-text cited sources at `>=30` unique references.

## References

If you need detailed review criteria, read:

- `../research-review-and-revise/references/review_checklist.md`

If you need grounded writing rules, read:

- `../research-grounded-writing/references/grounded_writing_checklist.md`

If you need corpus layout and paper note templates, read:

- `../research-literature-curation/references/corpus_layout.md`
- `../research-literature-curation/references/paper_note_template.md`
- `../research-literature-curation/references/source_mode_decision_template.md`
- `../research-literature-curation/references/manual_search_task_sheet_template.md`

For lightweight full-text retrieval over the local paper corpus, use:

- `../research-literature-curation/scripts/search_corpus.ps1`
- `../research-literature-curation/scripts/validate_notes_quality.py`

For artifact validation and resumability metadata, use:

- `scripts/validate_artifacts.py`

For packet completeness, placeholder, and language checks, use:

- `../research-grounded-writing/scripts/validate_section_packets.py`
