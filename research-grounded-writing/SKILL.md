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
7. Use a two-layer writing artifact model:
   - `section_packets/<section-id>.md` for evidence and argument backbone
   - `subsection_drafts/<section-id>.md` for full subsection prose

Precondition gate:

- if per-paper notes are still template placeholders or effectively empty, stop and request notes completion first
- if full-text readability is unresolved for key sources, report the blocker before drafting

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
5. draft full subsection prose into `subsection_drafts/<section-id>.md` from the packet
6. critique the subsection draft for thinness, missing evidence, weak comparison, and unsupported claims
7. if the subsection is still thin, run one supplemental retrieval pass using the gap revealed by the critique
8. update the packet and rewrite `subsection_drafts/<section-id>.md`
9. mark subsection draft status (`ready` or `blocked`) and only merge ready drafts into full report
10. run conformance and citation-whitelist checks before moving to full-document revision
11. run a subsection stance pass: ensure each subsection has a clear claim-first opening sentence (internal helper labels allowed in draft stage)
12. run a hedge cleanup pass: keep caveats as conditional applicability constraints, not as fence-sitting conclusions

This is the main lesson to inherit from the strongest open-source systems:

- section-level retrieval before drafting
- subsection-level drafting
- subsection packets as explicit evidence bundles
- bounded critique and repair
- attribution after content stabilizes

## Two-layer writing contract

`section_packets/<section-id>.md` should answer:

- what this subsection must prove
- which sources can support each claim
- what caveats must be retained
- what evidence is still missing

`subsection_drafts/<section-id>.md` should contain:

- complete prose for this subsection
- explicit citation handles
- a short self-check block (`evidence_coverage`, `overclaim_risk`, `needs_retrieval_reopen`)

Do not directly write `detailed_report.md` from a thin packet.
For substantial writing, draft subsection prose in `subsection_drafts` first, then merge.

When a local corpus is available, prefer using:

- `../research-literature-curation/scripts/search_corpus.ps1`

Run it with a subsection-specific query before drafting important subsections.
Store the strongest hits in the packet instead of relying only on memory or already-summarized notes.

## Section packet contract

For substantial writing, each `section_packets/<section-id>.md` should include:

- subsection title
- section goal
- retrieval budget (`top_k_per_query`, `min_unique_sources`, `max_sibling_source_overlap_ratio`)
- relevant notes
- relevant source ids
- key claims
- caveats

Packet set completeness is mandatory for substantial writing:

- generate packets for all required outline nodes (usually all substantive `1.1.1+` subsections, or project-defined depth)
- do not proceed with only a partial packet subset unless the user explicitly requests partial drafting
- template-created packets are not considered complete until required fields are filled with non-placeholder content

Before drafting the full report, run:

- `scripts/validate_section_packets.py --outline <refined_outline.md> --packets-dir <section_packets> --min-level 3 --report <section_packet_validation_report.md>`

Use script initialization when packet count is large:

- `scripts/init_section_packets.py`

If packet validation fails on missing files or placeholders, fix packets first and only then continue drafting.
If upstream notes quality validation fails, do not continue as if reading were complete.

## Subsection adequacy rule

In a detailed survey report:

- each non-trivial subsection should normally contain at least one substantive paragraph
- each analytical `subsection_drafts/<section-id>.md` should normally contain at least `2` prose paragraphs in `## Grounded Draft`
- each prose paragraph should normally contain at least `3` sentences (recommended `5+` for major subsections)
- important analytical subsections should usually contain `2+` distinct claims or comparison points
- each analytical subsection should usually cite at least `2` unique sources; core argument subsections should usually cite `3+`
- each analytical subsection should include explicit discussion of caveats, counterpoints, or boundary conditions (not only positive claims)
- if a subsection ends up with only one flat sentence, either expand it from evidence or merge it back into its parent

Exceptions are allowed for:

- short framing subsections
- transition subsections that are intentionally brief

## Retrieval-first rule for subsection drafts

Before writing `subsection_drafts/<section-id>.md`:

- run at least one subsection-specific local corpus query (for example via `search_corpus.ps1`)
- record query terms and strongest hits in the paired packet (or in `corpus_queries/<query-id>.md`)
- if retrieval returns no usable evidence for the subsection goal, mark subsection status as `blocked` and report the blocker before merge

For thin drafts, run one bounded reopen pass:

- targeted query expansion
- packet update
- subsection rewrite

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
- `subsection_drafts/<section-id>.md`

Then write the section.

## Final assembly gate

During final `detailed_report.md` assembly:

- do not introduce new factual claims that are absent from packet evidence
- if a new claim is needed, reopen that subsection loop (`retrieve -> packet update -> subsection_draft update`) before merge
- do not silently improvise new evidence in the final merge pass
- each analytical subsection in the merged report should retain an explicit claim-first sentence
- caveat discussion should appear after the main claim and should answer `where/when this claim may weaken`, not replace the main claim
- avoid merge artifacts that repeatedly output generic "this section has boundaries" language without concrete conditions
- remove process/helper labels from publication prose:
- do not keep `本节主张：...` in final report files
- do not mention workflow internals such as `section packet`, `subsection draft`, `this run`, `prompt`, `agent step` in abstract/body/conclusion
- abstract and conclusion must read like formal paper prose, not pipeline logs

Thinking is always allowed; unlogged evidence expansion is not.

## Claim-first synthesis rule

For final report prose (not packet notes):

- each analytical subsection should open with a clear position sentence
- keep one dominant claim per subsection and organize supporting evidence around it
- do not present two opposite conclusions as co-equal endpoints
- when limits exist, express them as applicability conditions, scope limits, or implementation prerequisites
- avoid using uncertainty language as the final sentence of a subsection unless evidence is genuinely unresolved
- if helper labels were used during drafting, strip them during final merge

## Language lock rule

Packet language should match the target draft language:

- if target draft is Chinese, keep packet goals/claims/caveats primarily in Chinese
- if target draft is English, keep packet goals/claims/caveats primarily in English
- source ids, citation handles, and command tokens can remain in English

For language-sensitive runs, run:

- `scripts/validate_section_packets.py --outline <refined_outline.md> --packets-dir <section_packets> --min-level 3 --language zh --report <section_packet_validation_report.md>`

Do not:

- invent comparisons that the sources do not support
- smooth over conflicting evidence without saying so
- cite a source that was not actually used
- imply full coverage when the screened corpus is still incomplete
- ignore an existing refined outline when writing a detailed report
- skip local corpus retrieval for a thin analytical subsection when full-text paper folders are available
- collapse packet and prose into a single file when subsection-level traceability is required

## Optional sub-agent drafting mode

When subsection count is large, sub-agents may draft in parallel:

- assign disjoint ownership by subsection-id
- each sub-agent edits only `subsection_drafts/<section-id>.md` (and optionally its paired packet)
- primary agent reviews all returned drafts for style consistency, duplication, and unsupported claims before merge
- prefer small-batch assignment (for example `4-10` subsections per round) over one-shot massive assignment
- after each batch, verify process evidence (`round1/round2`, query logs, citation floor, paragraph/sentence floor) before assigning next batch

## Coherence pass

After subsection drafting, run one adjacency coherence pass:

1. even-indexed subsections pass
2. odd-indexed subsections pass

Focus only on transitions, local redundancy, and contradiction carryover.
Record edits in `coherence_edits.md`.

## Structural checks

Before final review, run:

- `scripts/check_outline_conformance.py` to compare `refined_outline.md` and draft headings
- `scripts/check_citation_whitelist.py` to ensure subsection citations stay inside packet evidence scope
- `scripts/validate_subsection_drafts.py --drafts-dir <subsection_drafts> --report <subsection_draft_validation_report.md>`

Recommended outputs:

- `outline_conformance_report.md`
- `citation_whitelist_report.md`
- `subsection_draft_validation_report.md`

## Citation policy

During drafting, prefer stable source handles such as:

- `[@source-id]`

For substantial survey/course papers, enforce a corpus-level citation floor:

- if total collected records are `<15`, keep all collected sources, and prompt supplementation to at least `15`
- if total collected records are `15-29`, keep all collected sources and cite all included sources in the body text
- if total collected records are `>=30` and screening is used, keep final body-text citations at `>=30` unique sources
- when citation count is below the applicable target, add evidence-backed content rather than padding citation lists

Then optionally normalize citations with:

- `scripts/normalize_citations.py`

And render a references section with:

- `scripts/render_references.py`

## Checklist

Read:

- `references/grounded_writing_checklist.md`
- `references/subsection_draft_template.md`
