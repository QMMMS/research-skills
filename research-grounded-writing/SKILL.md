---
name: research-grounded-writing
description: Section-level, source-grounded drafting for surveys, literature reviews, and related-work writing. Use when the user wants writing tied explicitly to sources and evidence.
---

# Research Grounded Writing

Use this skill when prose must stay close to sources.

Typical triggers:

- "draft this survey section"
- "write a grounded related-work section"
- "turn these notes into a structured literature review"

## Core method

1. Work section by section, not full-document all at once.
2. For each section, identify the exact sources and claims it will use.
3. Draft from evidence, not from memory.
4. Mark citations or source handles during drafting.
5. Leave uncertainty explicit if evidence is weak or conflicting.
6. Revise for clarity only after evidence alignment is acceptable.

## Drafting contract

Before drafting a section, explicitly identify:

- section goal
- claims to make
- sources supporting each claim
- gaps or unresolved disputes

Then write the section.

Do not:

- invent comparisons that the sources do not support
- smooth over conflicting evidence without saying so
- cite a source that was not actually used

## Citation policy

During drafting, prefer stable source handles such as:

- `[@source-id]`

Then optionally normalize citations with:

- `scripts/normalize_citations.py`

And render a references section with:

- `scripts/render_references.py`

## Checklist

Read:

- `references/grounded_writing_checklist.md`
