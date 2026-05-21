#!/usr/bin/env bash
set -euo pipefail

has() {
  command -v "$1" >/dev/null 2>&1
}

need_install=0
for bin in latexmk xelatex bibtex; do
  if ! has "$bin"; then
    need_install=1
  fi
done

if [ "$need_install" -eq 0 ]; then
  echo "LaTeX toolchain is already installed."
  latexmk -v | head -n 1 || true
  xelatex --version | head -n 1 || true
  exit 0
fi

echo "Installing a XeLaTeX + latexmk toolchain."

require_sudo() {
  if [ "$(id -u)" -eq 0 ]; then
    return 0
  fi
  if ! has sudo; then
    echo "sudo is required for this installer, but sudo was not found."
    exit 1
  fi
  if [ ! -t 0 ] && ! sudo -n true 2>/dev/null; then
    cat <<'MSG'
This installer needs administrator privileges.

Run it from an interactive terminal so sudo can ask for your password:
  bash scripts/setup.sh
MSG
    exit 1
  fi
  sudo -v
}

if has apt-get; then
  require_sudo
  sudo apt-get update
  sudo apt-get install -y latexmk texlive-xetex texlive-latex-recommended texlive-latex-extra texlive-lang-chinese fonts-noto-cjk
elif has dnf; then
  require_sudo
  sudo dnf install -y latexmk texlive-xetex texlive-collection-latexextra texlive-collection-langchinese google-noto-sans-cjk-fonts
elif has pacman; then
  require_sudo
  sudo pacman -Sy --needed texlive-binextra texlive-latex texlive-latexextra texlive-langchinese noto-fonts-cjk
elif has brew; then
  if ! has tlmgr; then
    brew install --cask mactex-no-gui
    echo "Restart the terminal after MacTeX finishes installing, then run this script again."
    exit 0
  fi
  require_sudo
  sudo tlmgr update --self
  sudo tlmgr install latexmk ctex fontset fandol latex-bin collection-latexrecommended collection-latexextra
elif has tlmgr; then
  require_sudo
  sudo tlmgr update --self
  sudo tlmgr install latexmk xetex ctex fontset fandol collection-latexrecommended collection-latexextra
else
  cat <<'MSG'
No supported package manager was found.

Install TeX Live or MiKTeX manually, then make sure these commands exist:
  latexmk
  xelatex
  bibtex
MSG
  exit 1
fi

echo "Checking installed tools..."
for bin in latexmk xelatex bibtex; do
  command -v "$bin" >/dev/null
done

echo "Setup complete. Build with: make build"
