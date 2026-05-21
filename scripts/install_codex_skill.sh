#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skill_name="latex-doctor-fix"
source_dir="$repo_root/codex-skills/$skill_name"
dest_root="${CODEX_HOME:-$HOME/.codex}/skills"
dest_dir="$dest_root/$skill_name"

if [ ! -d "$source_dir" ]; then
  echo "Skill source not found: $source_dir" >&2
  exit 1
fi

mkdir -p "$dest_root"

if [ -e "$dest_dir" ]; then
  backup_dir="$dest_dir.backup.$(date +%Y%m%d-%H%M%S)"
  mv "$dest_dir" "$backup_dir"
  echo "Existing skill backed up to: $backup_dir"
fi

cp -R "$source_dir" "$dest_dir"

echo "Installed Codex skill: $skill_name"
echo "Location: $dest_dir"
echo "Restart Codex or start a new session if the skill list was already loaded."
