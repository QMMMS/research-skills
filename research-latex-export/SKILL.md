---
name: research-latex-export
description: Export survey, literature-review, and research-report artifacts into a LaTeX project with `.tex`, `.bib`, and optional `.pdf` outputs. Use when Codex needs to turn `draft_report.md`, `detailed_report.md`, `revised_report.md`, `section_packets`, or paper-folder BibTeX files into a compile-ready LaTeX manuscript, or when the user asks for a default academic template, LaTeX export, or PDF generation for research writing outputs.
---

# Research LaTeX Export

Use this skill at the final publication-oriented stage, after source collection, outlining, drafting, and revision already exist.

This skill is for:

- exporting Markdown-first research artifacts into a LaTeX project
- collecting BibTeX from paper folders into a single `references.bib`
- applying a default generic survey template or a user-provided template
- compiling the project into PDF when a local TeX environment is available

Do not use this skill for:

- early-stage literature curation
- outline design
- source-grounded drafting from scratch
- polishing an already-existing `.tex` paper project

For existing `.tex` projects, prefer the dedicated local skill:

- `latex-paper-en`

## Design policy

Follow two operating modes:

1. Export-only mode
   - generate `.tex` and `.bib`
   - do not require TeX to be installed
2. Export-and-compile mode
   - generate `.tex` and `.bib`
   - compile `.pdf` only if the toolchain is available or the user explicitly wants compilation

Treat local TeX availability as an environment fact, not as a hidden assumption.
Check for `latexmk`, `pdflatex`, `bibtex`, or `biber` before promising PDF output.

## Template policy

Use template priority in this order:

1. user-provided venue or lab template
2. repository default template

The bundled default template is intentionally generic.
It is suitable for:

- internal survey drafts
- reading reports
- advisor-facing review drafts
- generic academic manuscripts

It is not a substitute for venue-specific templates such as:

- NeurIPS
- ICML
- ACL
- IEEE
- ACM

If the user wants submission-ready formatting, ask for or locate the venue template instead of forcing the default one.

## Inputs

Prefer one of these as the main writing source:

- `revised_report.md`
- `detailed_report.md`
- `draft_report.md`

Optional supporting inputs:

- `refined_outline.md`
- `section_packets/<section-id>.md`
- `papers/<paper-id>/bib.txt`
- a user-supplied `.tex` template
- a user-supplied `.bib` file

## Workflow

1. Choose the source report to export.
2. Choose the template:
   - user template if available
   - bundled default template otherwise
3. Prepare the export source:
   - remove workflow and process meta-writing from final prose
   - flatten the final-paper introduction into continuous paragraphs
   - exclude any manual references appendix from the LaTeX body export when `.bib` will be used
4. Export the source report into `main.tex` body content.
5. Collect BibTeX entries from paper folders or a provided bibliography file.
6. Write a LaTeX project directory such as:
   - `latex/main.tex`
   - `latex/references.bib`
7. Run export audit before compilation:
   - detect raw Markdown heading leaks like `##`
   - detect unresolved raw citation markers like `[@paper-id]`
   - detect workflow/meta phrases leaking into the paper
   - write `export_audit.md`
   - treat any finding as a failed export until repaired
8. If compilation is desired, detect the local TeX toolchain.
9. Compile with `latexmk` when available.
10. If `latexmk` is unavailable, fall back to `pdflatex` plus `bibtex` when possible.
11. Run citation audit after compilation:
   - parse undefined citation keys
   - write `citation_gaps.md`
   - treat unresolved citations as a failed export unless explicitly overridden
12. Run paragraph-level citation audit:
   - detect long uncited paragraphs
   - write `paragraph_citation_gaps.md`
13. Parse first LaTeX compile error into `compile_error.json` for deterministic repair loops.
14. If `pdftotext` is available, extract the compiled PDF text for review.
15. Manually read the exported output end to end:
   - confirm the introduction has no internal subsection headings
   - confirm no raw `[@...]` citations remain
   - confirm no workflow/meta statements remain in abstract, body, or conclusion
   - confirm section numbering is publication-style rather than duplicated numbering artifacts
16. If unresolved citations or structural leaks remain, repair and recompile.

## Output contract

When this skill runs successfully, leave behind:

- `latex/main.tex`
- `latex/references.bib`
- optionally `latex/main.pdf`
- optionally `latex/build.log`
- `latex/compile_error.json`
- `latex/citation_gaps.md`
- `latex/paragraph_citation_gaps.md`
- `latex/export_audit.md`
- optionally `latex/main.pdf.txt`

If a user template is used, record that in a short note such as:

- `latex/template_choice.md`

## Scripts

Use these bundled scripts:

- `scripts/export_markdown_to_latex.py`
- `scripts/collect_bibtex.py`
- `scripts/compile_latex_project.py`
- `scripts/audit_paragraph_citations.py`

## Default assets

The bundled default template lives in:

- `assets/default-survey-template/main.tex.template`

## Practical rules

- Preserve heading hierarchy from the refined outline when exporting, except that the final-paper introduction should be continuous prose rather than a stack of internal subsections.
- Strip inline numbering prefixes from Markdown headings (for example `4.1 ...`, `5.2.1 ...`) and let LaTeX own structural numbering.
- If the first Markdown H1 duplicates the document title, skip that heading in the LaTeX body to avoid title/section duplication.
- Convert source handles like `[@paper-id]` into `\cite{paper-id}`.
- Normalize bare arXiv IDs to citation keys like `arxiv_2308_11432` to avoid BibTeX key edge cases.
- Remove backticks that wrap pure citation tokens before export so code formatting does not block citation conversion.
- Exclude manual reference lists from the body when the manuscript already uses BibTeX for the bibliography.
- Final-paper prose must not contain workflow/meta phrases such as `section packet`, `subsection draft`, `文献样本采用已收集`, or `实现全样本覆盖引用`.
- Prefer a generic, stable preamble over a package-heavy one.
- Do not promise venue compliance from the default template.
- If TeX is not installed, still finish the export stage instead of stopping.
- If BibTeX entries are duplicated, deduplicate by citation key and keep the first complete entry.
- Build should not be considered successful when `citation_gaps.md` lists unresolved keys.
- Build should not be considered structurally clean if headings appear as duplicated numbering patterns like `1.1.1 1.1 ...`.
- Build should not be considered complete until Codex has manually read the exported output, not only the audit files.
- Build should not be considered debuggable unless `compile_error.json` is generated when compilation fails.

## References

Read only when needed:

- `references/workflow.md`
- `references/template_policy.md`
