---
name: research-latex-zjuthesis
description: Use the bundled sanitized `zjuthesis` demo asset to show users how to fill required fields and compile a simple course-paper template. Use when Codex needs to point out which files and macros to edit, how to rebuild the project, and what minimal information still needs to be filled. This is a lightweight teaching template, not a formal graduation-thesis workflow.
---

# Research LaTeX ZJUThesis

Use this skill only for the simplified `zjuthesis`-style course-paper template packaged as a bundled asset.

Do not use this skill for:

- formal undergraduate or graduate thesis submission polishing
- GB/T 7714 compliance review for a real dissertation
- generic survey-export workflows

This template is a lightweight example, not a final graduation-thesis standard.
For official usage, tell the user to search the public `zjuthesis` GitHub repository and confirm the current upstream instructions.

## Bundled asset

This skill ships with a sanitized demo project:

- `assets/zjuthesis-template/`

The asset has already been scrubbed of project-specific personal information and reduced to a minimal example.
Do not treat personal-information cleanup as part of the user workflow for this skill.

## Scope

This skill is for:

- mapping where the template fields live
- copying the bundled demo asset into the current writable workspace before edits
- telling the user which fields still need to be filled
- explaining how to compile the copied project
- doing a light post-compile check only

## Required policy

- Treat the bundled asset as the starting point.
- If edits are needed, first copy the bundled asset into the current writable workspace.
- Do not modify the user's original external template in place.
- Keep the demo content intentionally small.
- Keep only one or two citations in the body unless the user explicitly wants more.

## Known project mapping

Read [references/zjuthesis-template-map.md](references/zjuthesis-template-map.md) when working on this template.

That reference contains the exact field mapping for:

- the cover label
- Chinese and English titles
- student name
- major and department
- submit date
- abstract
- running header
- bibliography database and print location
- compile recipe and output directory

## Standard workflow

1. Copy the bundled asset into the current writable workspace before editing.
2. Tell the user which fields in the copied project still need to be filled:
   - Chinese title
   - English title
   - name
   - major
   - department
   - submit date
   - abstract
3. Explain where the cover label and running header come from.
4. Compile using the configured recipe:
   - `xelatex -> biber -> xelatex -> xelatex`
   - output directory should be `out`
5. Run a light compile check:
   - the PDF exists under `out`
   - no undefined citation warnings remain in the final log
   - bibliography renders if citations are kept
6. Report back where each key field is filled and how to rebuild.

## What the bundled asset already contains

The sanitized asset already includes:

- a neutral cover label
- demo Chinese and English titles
- demo name, major, department, and submit date
- a minimal abstract: `这是摘要。`
- a minimal body with only a few headings and one or two citations

That content is there only to make the template self-explanatory and compilable.
Users can replace it after copying.

## Compile guidance

Prefer the project's configured build chain first:

- VS Code recipe `bibxe`
- or equivalent command sequence:
  - `xelatex -output-directory=out zjuthesis.tex`
  - `biber out/zjuthesis`
  - `xelatex -output-directory=out zjuthesis.tex`
  - `xelatex -output-directory=out zjuthesis.tex`

If `latexmk` is available and already used by the template, it is acceptable to use the template's documented command as an equivalent shortcut, but keep the reported explanation aligned with the VS Code recipe because that is what this project exposes in `.vscode/settings.json`.

## Output contract

When this skill is used successfully, report:

- that the bundled asset is already sanitized
- whether the asset had to be copied first
- which file contains each field the user must edit
- the exact compile path
- where the output PDF is generated
- whether the final compile check passed

## Practical rules

- Be explicit that this is a simple teaching template, not a formal thesis standard.
- If the user wants official thesis formatting, redirect them to the upstream `zjuthesis` project rather than pretending this demo copy is authoritative.
- Keep instructions concrete and file-based.
- Prefer telling the user exactly which file and macro to edit.




