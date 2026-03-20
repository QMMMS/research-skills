---
name: research-literature-curation
description: Multi-perspective literature collection and evidence organization for research tasks. Use when the user wants source discovery, source triage, evidence mapping, or literature-review preparation.
---

# Research Literature Curation

Use this skill when the task is primarily about gathering and structuring sources.

Typical triggers:

- "collect papers on X"
- "help me survey this topic"
- "find the main research threads"
- "build a reading list"
- "organize evidence before writing"

## Core method

1. Define topic boundaries.
2. Generate 3 to 6 perspectives or research angles.
3. For each perspective, write a small set of search questions.
4. Search and collect candidate papers.
5. Triage the papers into:
   - must-read
   - useful background
   - probably out-of-scope
6. Extract evidence into a structured inventory.
7. Build an evidence map that can be reused by later writing stages.

## Perspective generation

Avoid roleplay. Do not simulate fake experts unless that meaningfully improves the task.

Instead, explicitly generate research perspectives such as:

- taxonomy
- methodology
- datasets or benchmarks
- evaluation criteria
- limitations
- applications
- open problems

## Source inventory

For each retained source, capture at least:

- stable source id
- title
- year
- venue or arXiv id if available
- why it matters
- what claims or sections it supports

Use the template in:

- `references/source_inventory_template.md`

## Evidence mapping

Build `evidence_map.json` or equivalent notes that connect:

- section or question
- relevant sources
- key claims
- caveats

This skill should prepare later drafting, not only collect URLs.

## Scripts

If a simple arXiv search is enough, use:

- `scripts/search_arxiv.py`

Do not build a local paper database unless the user explicitly wants that engineering overhead.
