# Workflow Notes

Use this skill after the writing has already stabilized.

Recommended source priority:

1. `revised_report.md`
2. `detailed_report.md`
3. `draft_report.md`

If a refined outline exists, the exported LaTeX heading structure should preserve it.

Suggested export directory:

```text
latex/
  main.tex
  references.bib
  build.log
  citation_gaps.md
  main.pdf
```

If the user later switches to a venue template, keep the exported body and bibliography and replace only the scaffold layer.

After each compile pass, inspect undefined citations and create `citation_gaps.md`.
If unresolved citations remain, repair key mapping and compile again.
