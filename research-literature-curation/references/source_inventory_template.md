# Source Inventory Template

Use one entry per source.

```json
{
  "id": "source-short-id",
  "title": "Paper title",
  "year": 2025,
  "venue": "Venue or arXiv",
  "url": "https://...",
  "pdf_url": "https://...",
  "tags": ["personalization", "episodic-memory"],
  "summary": "Two or three sentences.",
  "bib": "@article{...}",
  "why_it_matters": "One or two sentences.",
  "supports": [
    "section or question 1",
    "section or question 2"
  ],
  "key_points": [
    "Point 1",
    "Point 2"
  ],
  "limitations": [
    "Limitation 1"
  ]
}
```

Minimum rule:

- do not keep a source without recording why it matters
- do not keep a claim without at least one supporting source
- do not mark a paper as full-text read without leaving a structured note
