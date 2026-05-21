# Agent Instructions

This repository is a LaTeX paper project intended for editing from Cursor or other agentic coding tools.

- Edit paper content in `sections/*.tex`, `main.tex`, and `references.bib`.
- Keep generated files out of git. Do not edit `build/`, `*.aux`, `*.log`, `*.bbl`, or `*.synctex.gz`.
- Build with `make build` before claiming the paper compiles.
- Run `make doctor` after edits. It validates project structure and runs a PDF build when LaTeX tools are installed.
- Use `make watch` for repeated local editing because `latexmk` recompiles only what changed.
- Keep figures in `figures/` and tables or CSV exports in `tables/`.
- Prefer small, focused edits that preserve labels, citations, and cross references.
- When adding a section, create `sections/<name>.tex` and include it from `main.tex`.
- To import an existing paper zip, run `make import-zip ZIP=/path/to/paper.zip`, then inspect `main.tex`, any imported files under `sections/`, and run `make doctor`.
