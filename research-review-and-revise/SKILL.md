---
name: research-review-and-revise
description: Review and revision workflow for research drafts, literature reviews, and survey writing. Use when Codex needs critique, coverage-gap detection, corpus adequacy checks, citation checking, or a structured revision pass.
---

# Research Review And Revise

Use this skill after a draft already exists.

Typical triggers:

- "review this literature review"
- "find coverage gaps"
- "check whether claims are grounded"
- "revise this survey draft"

## Review order

Run review in this order:

1. Scope alignment
2. Corpus adequacy
3. Coverage
4. Structure
5. Grounding and citation support
6. Overclaiming, unsupported synthesis, and fence-sitting language
7. Clarity and redundancy
8. Revision plan

Keep findings concrete and revision-oriented.

## Review output

Prefer a review note file such as `review_notes.md` with:

- major issues
- corpus weaknesses
- missing evidence
- duplicated sections
- claims needing softer wording
- sections lacking a clear claim-first sentence
- sections where caveats replace, rather than qualify, the core claim
- process-language leaks (for example `本节主张`, `section packet`, `this run`) appearing in publication prose
- workflow/meta phrasing in paper text (for example `本次语料库`, `课程论文写作`, `按本流程`)
- revision priorities

Then produce a revised draft or a targeted revision plan.

For substantial projects, keep critique items structured:

- `feedback`
- `severity` (`high`, `medium`, `low`)
- `followup_query` (if evidence gap exists)
- `must_retrieve` (`true`/`false`)
- `skip_retrieval_reason` (required when `must_retrieve=false`)

## Revision rules

- Fix evidence and coverage problems before polishing prose.
- Do not silently remove nuance just to make the text smoother.
- Preserve explicit uncertainty when the sources are mixed.
- If citations are malformed, fix the citation layer after content changes stabilize.
- Keep both `draft_report_raw.md` and `draft_report_refined.md` when large revisions are applied.
- Leave `revision_delta.md` for claim-level and citation-level change trace.
- For each analytical subsection, enforce one explicit claim-first sentence in the revised draft.
- Rewrite caveat-heavy endings into conditional statements that qualify a clear conclusion, instead of ending on an undecided stance.
- In final publication-facing files, remove draft helper labels and workflow/meta wording from abstract, body, and conclusion.

## Quality gate

Before publication export, score and gate:

- coverage
- structure
- relevance
- citation precision (and recall if available)
- unique body-cited source count (target depends on corpus size policy)

Use:

- `scripts/quality_gate_scorecard.py`

Typical thresholds:

- coverage >= 3
- structure >= 3
- relevance >= 3
- citation precision >= 0.60
- if total collected records are `<15`: prompt supplementation to at least `15`, and cite all included sources
- if total collected records are `15-29`: cite all included sources
- if total collected records are `>=30` and screening is used: unique body-cited sources >= 30

If the corpus is below 15 collected records, record a supplementation prompt to reach at least 15 before finalizing.

## Checklist

Read:

- `references/review_checklist.md`
