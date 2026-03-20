# Research Skills for Codex

[中文说明 / README_zh](README_zh.md)

Lightweight, open-source research skills for Codex, designed for literature review, survey planning, grounded drafting, and revision. 🔎

## Overview

This repository packages a practical research-writing workflow into reusable Codex skills.

The suite is designed around a simple separation of concerns:

- skills hold workflow logic, artifact contracts, and review discipline
- scripts handle deterministic and repetitive tasks
- optional infrastructure remains optional rather than becoming a default dependency

The result is a skill suite that stays usable without requiring a paper warehouse, a custom reranker service, or a multi-agent runtime.

## What is included

- `research-survey-workflow`
  - End-to-end workflow for topic scoping, curation, outlining, drafting, and revision.
- `research-literature-curation`
  - Multi-perspective literature collection and evidence organization.
- `research-outline-synthesis`
  - Rough outline generation, merge, subsection expansion, and final cleanup.
- `research-grounded-writing`
  - Section-level drafting tied to sources and evidence.
- `research-review-and-revise`
  - Coverage, structure, citation, and revision checks.

## Workflow At A Glance

The full workflow is organized as:

1. Scope the topic and deliverable
2. Curate sources and organize evidence
3. Synthesize a draft outline
4. Write section-level grounded text
5. Review for coverage, grounding, and structure
6. Revise and optionally normalize citations ✍️

Each stage is also available as a standalone skill.

## Why this structure

This repository does **not** attempt to recreate a full research-agent runtime.

Instead, it keeps the architecture modular:

- skills: reasoning workflow, artifact contracts, review discipline
- scripts: search, metadata collection, citation normalization, reference rendering
- optional infrastructure: local paper stores, rerankers, large indexes

## Recommended usage

Install all five skills together for the complete workflow.

Install individual skills when only one stage is needed:

- only source collection: `research-literature-curation`
- only outline generation: `research-outline-synthesis`
- only drafting: `research-grounded-writing`
- only review/revision: `research-review-and-revise`

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
```

Each skill only requires a `SKILL.md` file to function. This repository also includes optional scripts and references.

## Output conventions

The skills are designed around intermediate artifacts such as:

- `topic_scope.md`
- `research_questions.md`
- `source_inventory.json`
- `evidence_map.json`
- `draft_outline.md`
- `refined_outline.md`
- `draft_report.md`
- `review_notes.md`
- `revised_report.md`

These names are suggestions, not hard requirements.

## Design principles

This skill suite follows three defaults:

1. Prefer a simple workflow over a large runtime.
2. Prefer a small script over a heavy service.
3. Keep human review as an explicit checkpoint.

Accordingly, the core workflow works without:

- a local paper vector database
- a cross-encoder reranker service
- a custom training pipeline
- a multi-agent orchestration runtime

## Included scripts

- `research-literature-curation/scripts/search_arxiv.py`
  - Simple arXiv search helper.
- `research-grounded-writing/scripts/normalize_citations.py`
  - Convert source handles like `[@source-id]` into numeric citations.
- `research-grounded-writing/scripts/render_references.py`
  - Render a Markdown references section from a JSON file.

These scripts are intentionally small and replaceable.

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
```

## Minimal example

One practical usage pattern is:

1. Run `research-literature-curation` to collect sources and build an evidence map.
2. Run `research-outline-synthesis` to produce a draft and refined outline.
3. Run `research-grounded-writing` to draft section-level text with source handles.
4. Run `research-review-and-revise` to identify unsupported claims, structural overlap, and coverage gaps.
5. Use the citation scripts to normalize citations and render a references section if needed.

## Acknowledgements

This skill suite was informed by ideas from the following open-source projects:

- [STORM](https://github.com/stanford-oval/storm)
- [OpenScholar](https://github.com/AkariAsai/OpenScholar)
- [AutoSurvey](https://github.com/AutoSurveys/AutoSurvey)
- [Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory)

The goal here is not to repackage those projects, but to distill reusable workflow ideas for Codex skills.

## License

[MIT](LICENSE)
