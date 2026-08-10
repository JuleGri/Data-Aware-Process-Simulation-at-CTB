# AGENTS.md

## Repository overview
- This repository is a LaTeX dissertation project, not an application codebase.
- The main entrypoint is `dissertation.tex`.
- The custom document class is `Dissertate.cls`.
- Chapter content lives in `chapters/`.
- Front matter is stored in `frontmatter/`.
- Bibliography entries are in `references.bib`.
- Figures and static assets are in `figures/`, `resources/`, and `fonts/`.

## Editing guidance
- Prefer editing existing `.tex` sources instead of changing document structure unless the task requires it.
- Keep chapter filenames and `\include{...}` references aligned with the numbering pattern already used in `dissertation.tex`.
- Preserve the `%!TEX root = ../dissertation.tex` header when creating new chapter or frontmatter files.
- Place new figures under `figures/` and reference them with repository-relative LaTeX paths.
- Do not rename or replace bundled font or image assets unless explicitly required.
- Avoid committing generated LaTeX build artifacts.

## Validation
- `dissertation.tex` declares `xelatex` as the TeX program, so use XeLaTeX-compatible validation.
- If a full build is needed, validate from the repository root with `xelatex dissertation.tex`; rerun as needed for cross-references and bibliography resolution.
- When bibliography changes are involved, also run the repository's normal LaTeX bibliography flow before considering the change complete.
- For documentation-only edits that do not affect TeX structure, a content review may be sufficient when LaTeX tooling is unavailable.

## Repository-specific notes
- `frontmatter/personalize.tex` contains thesis metadata such as title, author, advisors, and academic year.
- The dissertation currently includes chapters `1.introduction` through `5.conclusion`.
- Two CSV files at the repository root appear to be thesis data artifacts; leave them unchanged unless the task is specifically about those datasets.
