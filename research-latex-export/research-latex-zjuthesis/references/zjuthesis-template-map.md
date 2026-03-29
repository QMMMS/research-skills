# ZJUThesis Template Map

This reference documents the bundled sanitized asset for the bundled simplified `zjuthesis` teaching template.

The asset lives at:

- `assets/zjuthesis-template/`

Use it only for this simplified template variant.

## Important positioning

This bundled asset is a sanitized teaching/demo template.
It is not the authoritative current official graduation-thesis format.
If a user needs a real thesis template, tell them to search the public `zjuthesis` GitHub repository.

## Entry and build

- Main entry file: `zjuthesis.tex`
- VS Code build config: `.vscode/settings.json`
- Output directory: `out`
- Exposed build chain: `xelatex -> biber -> xelatex -> xelatex`

## Main fields in `zjuthesis.tex`

These are passed through `\documentclass[...]` options:

- `StudentName = ...`
- `Major = ...`
- `Department = ...`
- `SubmitDate = ...`
- `Title = ...`
- `TitleEng = ...`
- `Degree = graduate`
- `GradLevel = master`
- `Type = thesis`

Optional multi-line helpers in the same file:

- `\titletwolines{...}{...}`
- `\titleengtwolines{...}{...}`
- `\majortwolines{...}{...}`
- `\departmenttwolines{...}{...}`

## Where the cover label comes from

The cover label and running-header label are driven by class-level macros:

- `\TitleTypeName`
- `\TitleTypeNameCover`

In the bundled sanitized asset, the original project-specific string has already been replaced with a neutral demo label.

## Cover rendering

The Chinese cover page is rendered through:

- `page/graduate/cover.tex`
- `page/graduate/cover-chn.tex`

That cover uses:

- `\TitleTypeNameCover`
- `\Title`
- `\TitleEng`
- `\StudentName`
- `\Major`
- `\Department`
- `\SubmitDate`

## Abstract

The graduate abstract page file is:

- `page/graduate/abstract.tex`

In the bundled asset it already contains a minimal example abstract.
Users can replace that text after copying the asset.

No dedicated keyword macro was found in the inspected graduate path.
For this simplified template, write keywords manually at the end of the abstract if needed.

## TOC

The table of contents is generated in:

- `page/graduate/toc.tex`

It calls:

- `\tableofcontents`

TOC generation is gated by the class option:

- `ListOfContents = true`

## Running header

The running header is configured in:

- `config/format/general/layout.tex`

For the graduate path, the left header is `\TitleTypeName` and the right header is the current chapter mark.
Therefore, changing the label macro affects both the cover and the running header.

## Bibliography

- Bibliography database file: `body/ref.bib`
- Print location for graduate path: `body/graduate/post/ref.tex`
- Print command: `\printbibliography`

So the normal chain is:

1. add entries to `body/ref.bib`
2. cite them in the body with `\cite{key}`
3. print them through the post file

## Example citation usage

The bundled graduate body uses `\cite{...}` in:

- `body/graduate/content.tex`

The bundled asset intentionally keeps only a very small number of citations.

## Recommended user-facing explanation

When guiding the user, say that they only need to replace:

- title
- English title
- name
- major
- department
- submit date
- abstract
- body text

The rest of the demo content exists only to keep the copied template compilable.



