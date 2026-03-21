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
2. Search for existing surveys, tutorials, or benchmark overviews and read them first.
3. Create `topic_scope.md` and `research_questions.md`.
4. Build an initial candidate pool, usually `80-150` papers for a serious survey.
5. Screen titles and abstracts down to a working set, usually `40-60` papers.
6. Produce full-text reading notes for a core set, usually `30-40` papers or more.
7. Organize corpus metadata, paper folders, and source inventory.
8. Add a lightweight local corpus retrieval layer over `papers/<paper-id>/...`.
9. Build an `evidence_map.json` or equivalent section-wise evidence notes.
10. Generate rough outlines from clustered notes.
11. Expand the outline into a refined multi-level outline.
12. For each section and subsection, create a `section_packets/<section-id>.md` evidence packet.
13. Run a local evidence retrieval pass against notes, metadata, and full-text corpus files, and record the result in the packet.
14. Draft section-level content grounded in the retrieved evidence.
15. Run a bounded critique pass on each section, retrieve supplemental evidence where needed, update the packet, and revise.
16. Review the full draft for corpus adequacy, coverage, structure, citation support, and overclaiming.
17. Revise the draft.
18. Optionally normalize citations and render a references section.
19. Optionally export the final draft into a LaTeX project and compile PDF with `research-latex-export`.

## Required habits

- Prefer explicit source-backed claims.
- Separate drafting from review.
- Keep intermediate artifacts on disk when the task is substantial.
- Stop and surface major evidence gaps instead of hallucinating around them.
- Ask for human judgment only at meaningful checkpoints, not after every micro-step.
- Treat existing surveys as starting points, not as substitutes for reading primary papers.
- Do not describe a survey as substantial if it lacks a screened corpus and full-text notes.
- Do not treat a one-level outline as a refined outline.

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
- each subsection should trigger its own local corpus retrieval step
- each subsection should be checked for thinness before moving on
- weak subsections should receive one bounded supplementary retrieval pass rather than being left as placeholder prose

## Output contract

When running the full workflow, try to leave behind:

### Phase 1: Scope and bootstrap

- `topic_scope.md`
- `research_questions.md`
- `existing_surveys.md`

### Phase 2: Corpus building

- `candidate_pool.json` or `candidate_pool.md`
- `screening_decisions.md`
- `source_inventory.json` or `source_inventory.md`
- `papers/<paper-id>/metadata.md`
- `papers/<paper-id>/notes.md`
- `papers/<paper-id>/bib.txt`
- `papers/<paper-id>/links.txt`

### Phase 3: Evidence and structure

- `evidence_map.json` or equivalent notes
- `draft_outline.md`
- `refined_outline.md`
- `section_evidence_index.md`
- `corpus_queries/<query-id>.md` when local corpus retrieval is material

### Phase 4: Writing and revision

- `section_packets/<section-id>.md`
- `draft_report.md`
- `detailed_report.md`
- `review_notes.md`
- `revised_report.md`

### Phase 5: Publication export

- `latex/main.tex`
- `latex/references.bib`
- `latex/build.log`
- `latex/main.pdf`

## Engineering defaults

Prefer lightweight operation by default:

- avoid local paper databases unless explicitly requested
- avoid heavy rerankers unless simple ranking is inadequate
- use small scripts for corpus retrieval and citation cleanup instead of large infrastructure

If the user wants a formal survey, prefer a traceable corpus layout over ad hoc notes.

## Corpus expectations

For a serious survey, aim for:

- initial candidate pool: `80-150`
- title and abstract screened set: `40-60`
- full-text notes: `30-40+`

These are workflow heuristics, not hard publication rules. If the topic is unusually narrow, record the reason for a smaller corpus instead of pretending the literature is larger than it is.

## References

If you need detailed review criteria, read:

- `../research-review-and-revise/references/review_checklist.md`

If you need grounded writing rules, read:

- `../research-grounded-writing/references/grounded_writing_checklist.md`

If you need corpus layout and paper note templates, read:

- `../research-literature-curation/references/corpus_layout.md`
- `../research-literature-curation/references/paper_note_template.md`

For lightweight full-text retrieval over the local paper corpus, use:

- `../research-literature-curation/scripts/search_corpus.ps1`
