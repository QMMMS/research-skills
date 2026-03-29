# Source Mode Decision Template

Use this template before starting retrieval.

## Topic

- topic:
- objective:
- target deliverable:

## Source mode

- selected_mode: `manual-gated` | `api-automated` | `hybrid`
- rationale:

## Source list

- source: `CNKI` | `arXiv` | `OpenAlex` | `Crossref` | ...
- access constraints:
- human-required steps:
- automation-allowed steps:

## Compliance boundary

- do_not_automate:
  - login bypass
  - captcha/slider bypass
  - anti-bot evasion
- manual_confirmed_by_user: yes/no

## Acquisition plan

- stage_a_survey_first: yes/no
- stage_b_topic_keyword: yes/no
- recommended_counts:
  - stage_a_surveys:
  - stage_b_candidates:
  - screened_set:
  - full_text_notes:

## Notes

- fallback strategy if access is limited:
- logging path for manual actions:
