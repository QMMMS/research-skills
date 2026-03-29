# Manual Search Task Sheet (Template)

Use this sheet when retrieval is human-gated (for example CNKI access with institutional login/captcha).

## Basic info

- date:
- operator:
- source:
- topic:

## Stage A: Survey-first retrieval

Goal: collect high-level surveys/reviews/tutorials first.

- recommended target: `8-20` records (not mandatory)
- required fields to capture per record:
  - title
  - url
  - year
  - venue
  - short note (why relevant)

Queries:

- A1:
- A2:
- A3:

## Stage B: Topic-keyword retrieval

Goal: collect topic-specific papers after Stage A map is clear.

- recommended target: `30-100` candidate records before screening (not mandatory)
- query schema:
  - core_terms:
  - expand_terms:
  - exclude_terms:
  - field:
  - year_range:

Queries:

- B1:
- B2:
- B3:
- B4:

## Download and citation format conventions

Preferred full text:

- `PDF` first
- `CAJ` fallback

Citation export priority:

1. `BibTeX`
2. `RIS`
3. EndNote-compatible plain text

## File drop locations

- full text files: `acq/inbox/raw/`
- citation exports: `acq/inbox/citations/`
- manual notes/log: `acq/manual_log.md`

## Completion checklist

- [ ] Stage A done
- [ ] Stage B done
- [ ] full text moved to inbox
- [ ] citations moved to inbox
- [ ] manual log updated
