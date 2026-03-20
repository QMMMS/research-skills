---
name: research-survey-workflow
description: End-to-end workflow for literature review, survey planning, grounded drafting, and revision. Use when the user wants a full research-writing pipeline rather than a single isolated step.
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
2. Create `topic_scope.md` and `research_questions.md`.
3. Collect sources and organize them into `source_inventory.json` or `source_inventory.md`.
4. Build an `evidence_map.json` or section-wise evidence notes.
5. Draft a rough outline.
6. Refine the outline.
7. Draft section-level content grounded in sources.
8. Review the draft for coverage, structure, citation support, and overclaiming.
9. Revise the draft.
10. Optionally normalize citations and render a references section.

## Required habits

- Prefer explicit source-backed claims.
- Separate drafting from review.
- Keep intermediate artifacts on disk when the task is substantial.
- Stop and surface major evidence gaps instead of hallucinating around them.
- Ask for human judgment only at meaningful checkpoints, not after every micro-step.

## Output contract

When running the full workflow, try to leave behind:

- `topic_scope.md`
- `research_questions.md`
- `source_inventory.json` or `source_inventory.md`
- `evidence_map.json` or equivalent notes
- `draft_outline.md`
- `refined_outline.md`
- `draft_report.md`
- `review_notes.md`
- `revised_report.md`

## Engineering defaults

Prefer lightweight operation by default:

- avoid local paper databases unless explicitly requested
- avoid heavy rerankers unless simple ranking is inadequate
- use small scripts for citation cleanup instead of large infrastructure

## References

If you need detailed review criteria, read:

- `../research-review-and-revise/references/review_checklist.md`

If you need grounded writing rules, read:

- `../research-grounded-writing/references/grounded_writing_checklist.md`
