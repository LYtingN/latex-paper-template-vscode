---
name: latex-doctor-fix
description: Diagnose and fix LaTeX paper-template build failures by running `make doctor`, interpreting LaTeX/Cursor Workshop errors, repairing common project issues, and rerunning verification. Use when the user asks Codex to run `make doctor`, fix LaTeX build errors, resolve missing images such as "Image Missing Check ...", clean generated auxiliary files, fix `\input`/`\include` paths, repair bibliography or figure path problems, or make `build/main.pdf` compile in this template.
---

# Latex Doctor Fix

## Workflow

Use this skill inside a LaTeX paper template repository that has `Makefile`, `scripts/doctor.sh`, `latexmkrc`, and `main.tex`.

1. Inspect the current state before editing:
   - Run `pwd`.
   - Run `find . -maxdepth 3 -type f | sort | sed -n '1,200p'`.
   - Run `make doctor` and keep the relevant failure lines.
   - If the failure mentions generated files outside `build/`, list them with:

```bash
find . -path './build' -prune -o -type f \( -name '*.aux' -o -name '*.log' -o -name '*.bbl' -o -name '*.blg' -o -name '*.bcf' -o -name '*.fdb_latexmk' -o -name '*.fls' -o -name '*.out' -o -name '*.run.xml' -o -name '*.synctex.gz' -o -name '*.toc' -o -name '*.xdv' \) -print
```

2. Fix the actual root cause, not only the final symptom.
   - Prefer existing template conventions: `main.tex`, `sections/`, `figures/`, `tables/`, `references.bib`, and `build/`.
   - Do not edit `build/` artifacts as source.
   - Remove only confirmed generated auxiliary files outside `build/`.
   - If a file is user content or could be source, preserve it and ask before deleting.

3. Re-run verification:
   - Run `make doctor`.
   - Confirm `build/main.pdf` exists.
   - If the user reported a visible placeholder or text symptom, verify the PDF text with `pdftotext build/main.pdf - | rg "..."` when `pdftotext` is available.
   - Run a narrow source search proving the bad reference is gone.

## Common Fixes

### Image Missing

If the PDF shows `Image Missing` or `Check <filename>`:

- Search source and assets:

```bash
rg -n "Image Missing|Check|safeincludegraphics|includegraphics|<filename>" main.tex sections figures imports -S
find figures imports -iname '*logo*' -o -iname '*.pdf' -o -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg'
```

- Check filename spelling, hyphen/underscore differences, and case sensitivity.
- Remember `\IfFileExists{file}` does not reliably search every `\graphicspath` entry. Use an explicit path like `figures/example-figure.pdf`, or update the helper macro to check `figures/#2`.
- If the importer caused the bad path, fix `scripts/import_latex_zip.py` too so re-importing does not recreate the same bug.

### Generated Files Outside build/

If `make doctor` fails because `.aux`, `.log`, `.bbl`, `.blg`, `.synctex.gz`, `.toc`, `.xdv`, or similar generated files are outside `build/`:

- Confirm the files are generated LaTeX artifacts, not source.
- Remove the exact generated files outside `build/`.
- Re-run `make doctor`.
- If generated files are repeatedly created in the root, inspect `latexmkrc` and ensure the output directory is `build`.

### Missing input/include

If `make doctor` reports missing `\input` or `\include` targets:

- Search for the referenced file under the repo.
- Prefer moving or rewriting references to `sections/<name>` according to the template layout.
- For imported zip projects, check `imports/original-source/` as the fallback source of truth.

### Bibliography

If BibTeX fails:

- Confirm `references.bib` exists and is not empty.
- Confirm `\bibliography{references}` or the project's expected bibliography command.
- Search `build/main.blg` and `build/main.log` for the first real BibTeX error.

### Missing tools

If `latexmk`, `xelatex`, or `bibtex` is missing:

- Tell the user the toolchain is missing.
- Run `make setup` only if the user has asked to install dependencies or approval is available, because setup may need network and administrator privileges.

## Final Response

Report:

- the root cause;
- files changed;
- the exact verification command, especially `make doctor`;
- any remaining warnings that do not block PDF generation.
