---
name: research-outline-synthesis
description: Outline-first planning for surveys, literature reviews, and related-work drafts. Use when Codex needs a strong multi-level structure before writing prose, especially after source screening, reading-note clustering, and evidence mapping.
---

# Research Outline Synthesis

Use this skill when the task is mainly about planning structure.

Typical triggers:

- "make an outline for a survey on X"
- "merge these outline ideas"
- "expand sections into subsections"
- "help me structure related work"

## Core method

1. Start from reading notes and evidence clusters, not from a generic template alone.
2. After every `5-8` deeply read papers, revisit the emerging themes and rewrite provisional headings.
3. Produce `2-4` rough outlines rather than committing too early.
4. Compare them for coverage, overlap, and missing contrasts.
5. Merge them into a single high-level outline.
6. Expand each major section into subsections and sub-subsections where needed.
7. Remove redundancy and reorder for narrative flow.
8. Produce a final outline that can drive section-level retrieval and writing.

Use a four-stage artifact chain for substantial surveys:

1. `rough_outlines.md` (or `rough_outline_a.md` + `rough_outline_b.md`)
2. `merged_outline.md`
3. `subsection_outline.md`
4. `refined_outline.md`

## How detailed the outline should be

For a substantial survey:

- the refined outline should use at least `2` heading levels
- if the corpus includes `20+` full-text paper notes, the refined outline should usually use `3` heading levels
- each major section should usually contain `2-5` subsections
- each subsection should map to a visible evidence cluster, not only to a vague topic label

Do not stop at:

- `1. Introduction`
- `2. Methods`
- `3. Evaluation`

That level is only acceptable for a rough outline, not for a refined survey outline.

## Where good subsections come from

Good subsection titles should emerge from repeated reading and clustering, not arbitrary decomposition.

Use this loop:

1. read a batch of papers
2. extract recurring mechanisms, tensions, benchmarks, and failure modes
3. group similar notes into clusters
4. turn clusters into subsection candidates
5. merge or split subsection candidates until each one has a clear claim and evidence base

Typical natural sources of subsection boundaries:

- different memory functions
- different update strategies
- different retrieval strategies
- different evaluation setups
- different failure modes
- different application constraints

## Rules

- Do not start with prose if structure is still weak.
- Do not finalize a formal survey outline before the full-text reading set is large enough.
- Do not keep overlapping sections with slightly different names.
- Prefer section titles that encode clear distinctions.
- If the task is a survey, make the outline reflect comparison axes, not just a chronological list.
- If a subsection cannot be supported by distinct evidence, merge it or remove it.
- Run outline lint before handing off to drafting for substantial reports.

## Recommended artifacts

- `rough_outlines.md` or `rough_outline_a.md` + `rough_outline_b.md`
- `outline_merge_notes.md`
- `merged_outline.md`
- `subsection_outline.md`
- `draft_outline.md`
- `refined_outline.md`
- `section_evidence_index.md`
- `outline_lint_report.md`

## Outline patterns

Read:

- `references/outline_patterns.md`

Use those patterns as heuristics, not as rigid templates.

## Script

Use:

- `scripts/lint_outline.py`

Typical check:

- duplicate sibling headings
- empty headings without body or children
- insufficient subsections for top-level sections
- sibling heading overlap risk
