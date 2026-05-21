MAIN ?= main
BUILD_DIR ?= build
LATEXMK ?= latexmk

.PHONY: all init build watch clean distclean setup check doctor import-zip install-skill

all: build

init: setup build

build:
	$(LATEXMK) $(MAIN).tex

watch:
	$(LATEXMK) -pvc $(MAIN).tex

clean:
	$(LATEXMK) -c $(MAIN).tex

distclean:
	$(LATEXMK) -C $(MAIN).tex
	rm -rf $(BUILD_DIR)

setup:
	bash scripts/setup.sh

check:
	@command -v latexmk >/dev/null || { echo "latexmk is missing. Run: make setup"; exit 1; }
	@command -v xelatex >/dev/null || { echo "xelatex is missing. Run: make setup"; exit 1; }
	@echo "LaTeX toolchain is ready."

doctor:
	bash scripts/doctor.sh

import-zip:
	@test -n "$(ZIP)" || { echo "Usage: make import-zip ZIP=/path/to/paper.zip"; exit 1; }
	python3 scripts/import_latex_zip.py "$(ZIP)"

install-skill:
	bash scripts/install_codex_skill.sh
