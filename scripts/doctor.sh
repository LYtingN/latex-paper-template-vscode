#!/usr/bin/env bash
set -euo pipefail

failures=0

pass() {
  printf '[ok] %s\n' "$1"
}

warn() {
  printf '[warn] %s\n' "$1"
}

fail() {
  printf '[fail] %s\n' "$1"
  failures=$((failures + 1))
}

need_file() {
  if [ -f "$1" ]; then
    pass "found $1"
  else
    fail "missing $1"
  fi
}

need_nonempty_file() {
  need_file "$1"
  if [ -s "$1" ]; then
    pass "$1 is not empty"
  else
    fail "$1 is empty"
  fi
}

need_dir() {
  if [ -d "$1" ]; then
    pass "found $1/"
  else
    fail "missing $1/"
  fi
}

need_nonempty_file main.tex
need_nonempty_file latexmkrc
need_nonempty_file Makefile
need_nonempty_file references.bib
need_nonempty_file README.md
need_nonempty_file AGENTS.md
need_nonempty_file scripts/import_latex_zip.py
need_nonempty_file scripts/setup.sh
need_nonempty_file scripts/doctor.sh
need_file .gitignore
need_nonempty_file .cursor/rules/latex-paper.mdc
need_file .vscode/settings.json
need_file .vscode/extensions.json
need_file .vscode/tasks.json
need_dir sections
need_dir figures
need_dir tables

if command -v jq >/dev/null 2>&1; then
  jq empty .vscode/settings.json .vscode/extensions.json .vscode/tasks.json
  pass "Cursor/VS Code JSON files are valid"
else
  warn "jq is not installed; skipping JSON validation"
fi

if grep -q '\\documentclass' main.tex && grep -q '\\begin{document}' main.tex && grep -q '\\end{document}' main.tex; then
  pass "main.tex has a complete document skeleton"
else
  fail "main.tex is missing documentclass, begin document, or end document"
fi

missing_inputs=0
while IFS= read -r input_path; do
  if [ ! -f "${input_path}.tex" ]; then
    printf '[fail] main.tex references missing input %s.tex\n' "$input_path"
    missing_inputs=$((missing_inputs + 1))
  fi
done < <(sed -n 's/.*\\input{\([^}]*\)}.*/\1/p' main.tex)

if [ "$missing_inputs" -eq 0 ]; then
  pass "all \\input files exist"
else
  failures=$((failures + missing_inputs))
fi

for bin in latexmk xelatex bibtex; do
  if command -v "$bin" >/dev/null 2>&1; then
    pass "$bin is installed"
  else
    warn "$bin is missing; run: make setup"
  fi
done

if command -v latexmk >/dev/null 2>&1 && command -v xelatex >/dev/null 2>&1; then
  echo "Running LaTeX build check..."
  latexmk main.tex
  test -f build/main.pdf
  pass "build/main.pdf was produced"
else
  warn "skipping PDF build because LaTeX tools are not installed"
fi

if find . \
  -path './build' -prune -o \
  -path './imports/backups' -prune -o \
  -type f \( -name '*.aux' -o -name '*.log' -o -name '*.bbl' -o -name '*.blg' -o -name '*.synctex.gz' \) \
  -print | grep -q .; then
  fail "generated LaTeX auxiliary files exist outside build/"
else
  pass "no generated LaTeX auxiliary files found outside build/"
fi

if [ "$failures" -gt 0 ]; then
  printf 'Doctor found %s problem(s).\n' "$failures"
  exit 1
fi

echo "Doctor checks passed."
