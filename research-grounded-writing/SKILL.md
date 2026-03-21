---
name: research-grounded-writing
description: Section-level, source-grounded drafting for surveys, literature reviews, and related-work writing. Use when Codex needs writing tied explicitly to sources, evidence maps, full-text reading notes, and a pre-defined multi-level outline.
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

For formal surveys, treat full-text notes as the primary drafting substrate and use abstract-only sources only for background or gap identification.
Do not treat `notes.md` as the only retrieval surface once a local paper corpus exists. For analytical subsections, retrieve against both structured notes and the full-text corpus under `papers/<paper-id>/src/`.

## Structure fidelity rule

If a refined outline already exists:

- draft the report by following its heading hierarchy directly
- preserve the section and subsection structure unless there is a clear reason to merge or split
- if you change the structure, update the outline first or leave a revision note explaining the mismatch

Do not produce a detailed report that collapses:

- `3.1 / 3.1.1 / 3.1.2`

into only:

- `3.1`

That is acceptable only for an early draft, not for a detailed survey report.

## Section drafting loop

For each subsection in a substantial survey, use this loop:

1. confirm the subsection title and drafting purpose
2. create or update a `section_packets/<section-id>.md` file for that subsection
3. retrieve the most relevant paper notes, metadata, and full-text passages for that subsection
4. record the retrieval result in the packet
5. draft a grounded paragraph or set of paragraphs from the packet
6. critique the subsection for thinness, missing evidence, weak comparison, and unsupported claims
7. if the subsection is still thin, run one supplemental retrieval pass using the gap revealed by the critique
8. update the packet and rewrite the subsection

This is the main lesson to inherit from the strongest open-source systems:

- section-level retrieval before drafting
- subsection-level drafting
- subsection packets as explicit evidence bundles
- bounded critique and repair
- attribution after content stabilizes

When a local corpus is available, prefer using:

- `../research-literature-curation/scripts/search_corpus.ps1`

Run it with a subsection-specific query before drafting important subsections.
Store the strongest hits in the packet instead of relying only on memory or already-summarized notes.

## Subsection adequacy rule

In a detailed survey report:

- each non-trivial subsection should normally contain at least one substantive paragraph
- important analytical subsections should usually contain `2+` distinct claims or comparison points
- if a subsection ends up with only one flat sentence, either expand it from evidence or merge it back into its parent

Exceptions are allowed for:

- short framing subsections
- transition subsections that are intentionally brief

## Drafting contract

Before drafting a section, explicitly identify:

- section goal
- claims to make
- sources supporting each claim
- paper-note locations if available
- corpus search results when local full-text retrieval was used
- gaps or unresolved disputes

Prefer leaving this information on disk in:

- `section_packets/<section-id>.md`

Then write the section.

Do not:

- invent comparisons that the sources do not support
- smooth over conflicting evidence without saying so
- cite a source that was not actually used
- imply full coverage when the screened corpus is still incomplete
- ignore an existing refined outline when writing a detailed report
- skip local corpus retrieval for a thin analytical subsection when full-text paper folders are available

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
