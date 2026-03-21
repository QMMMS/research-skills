# Corpus Layout

Use a traceable on-disk structure when the task is a substantial survey.

Recommended layout:

```text
run-name/
  topic_scope.md
  research_questions.md
  existing_surveys.md
  candidate_pool.json
  screening_decisions.md
  source_inventory.md
  evidence_map.md
  papers/
    paper-id/
      metadata.md
      notes.md
      bib.txt
      links.txt
      paper.pdf   # optional
```

Use `paper-id` values that are stable and readable, for example:

- `memgpt-2023`
- `generative-agents-2023`
- `memorybank-2023`

Minimum expectation for each paper folder:

- `metadata.md`: title, year, venue, tags, URL, PDF URL
- `notes.md`: structured reading notes
- `bib.txt`: BibTeX or equivalent citation
- `links.txt`: canonical links and project links

If the PDF is not downloaded, still keep the folder and record the PDF URL in `links.txt`.
