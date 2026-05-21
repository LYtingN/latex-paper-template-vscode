#!/usr/bin/env python3
"""Import an existing LaTeX zip archive into this project layout."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path


IMAGE_EXTS = {".pdf", ".png", ".jpg", ".jpeg", ".eps", ".svg"}
TABLE_EXTS = {".csv", ".tsv", ".xlsx", ".xls", ".dat"}
ROOT_SUPPORT_EXTS = {".cls", ".sty", ".bst", ".bbx", ".cbx", ".def", ".cfg"}
GENERATED_EXTS = {
    ".aux",
    ".bbl",
    ".bcf",
    ".blg",
    ".fdb_latexmk",
    ".fls",
    ".log",
    ".out",
    ".run.xml",
    ".synctex.gz",
    ".toc",
    ".xdv",
}


def read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def safe_extract(zip_path: Path, dest: Path) -> None:
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.infolist():
            if member.is_dir():
                continue
            member_path = Path(member.filename)
            if member_path.is_absolute() or ".." in member_path.parts:
                raise SystemExit(f"Unsafe zip entry: {member.filename}")
            archive.extract(member, dest)


def source_root(extracted: Path) -> Path:
    children = [p for p in extracted.iterdir() if not p.name.startswith("__MACOSX")]
    dirs = [p for p in children if p.is_dir()]
    files = [p for p in children if p.is_file()]
    if len(dirs) == 1 and not files:
        return dirs[0]
    return extracted


def score_tex(path: Path, root: Path) -> int:
    text = read_text(path)
    lower_name = path.name.lower()
    score = 0
    if "\\documentclass" in text:
      score += 100
    if "\\begin{document}" in text:
      score += 100
    if lower_name in {"main.tex", "paper.tex", "article.tex", "manuscript.tex"}:
      score += 35
    if path.parent == root:
      score += 10
    if "\\end{document}" in text:
      score += 20
    return score


def find_main_tex(root: Path) -> Path:
    candidates = tex_files(root)
    if not candidates:
        raise SystemExit("No .tex files found in the zip archive.")
    ranked = sorted(candidates, key=lambda p: score_tex(p, root), reverse=True)
    best = ranked[0]
    if score_tex(best, root) < 150:
        raise SystemExit("Could not identify a main LaTeX file with a document environment.")
    return best


def tex_files(root: Path) -> list[Path]:
    return [
        p for p in root.rglob("*.tex")
        if not any(part.startswith(".") for part in p.relative_to(root).parts)
    ]


def split_document(text: str) -> tuple[str, str]:
    begin = re.search(r"\\begin\{document\}", text)
    end = re.search(r"\\end\{document\}", text)
    if not begin or not end or end.start() <= begin.end():
        raise SystemExit("The detected main .tex file does not contain a complete document.")
    preamble = text[:begin.start()].rstrip()
    body = text[begin.end():end.start()].strip()
    return preamble, body


def backup_existing(project: Path, timestamp: str) -> Path:
    backup_dir = project / "imports" / "backups" / timestamp
    paths = [
        project / "main.tex",
        project / "references.bib",
        project / "sections",
        project / "figures",
        project / "tables",
    ]
    backup_dir.mkdir(parents=True, exist_ok=True)
    for path in paths:
        if not path.exists():
            continue
        target = backup_dir / path.name
        if path.is_dir():
            shutil.copytree(path, target, dirs_exist_ok=True)
        else:
            shutil.copy2(path, target)
    return backup_dir


def copy_tree_contents(src: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for path in src.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(src)
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def copy_support_files(root: Path, project: Path, main_tex: Path) -> None:
    sections = project / "sections"
    figures = project / "figures"
    tables = project / "tables"

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if path == main_tex:
            continue
        suffix = path.suffix.lower()
        if suffix in GENERATED_EXTS:
            continue
        if suffix == ".tex":
            target = sections / rel
        elif suffix == ".bib":
            target = project / path.name
        elif suffix in IMAGE_EXTS:
            target = figures / rel
        elif suffix in TABLE_EXTS:
            target = tables / rel
        elif suffix in ROOT_SUPPORT_EXTS:
            target = project / path.name
        else:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        if suffix in IMAGE_EXTS and "_" in target.name:
            alias = target.with_name(target.name.replace("_", "-"))
            shutil.copy2(path, alias)


def merge_bibliography(root: Path, project: Path) -> None:
    bib_files = sorted(root.rglob("*.bib"))
    if not bib_files:
        return
    parts = []
    for bib_file in bib_files:
        rel = bib_file.relative_to(root).as_posix()
        parts.append(f"% ---- Imported from {rel} ----\n")
        parts.append(read_text(bib_file).strip())
        parts.append("\n\n")
    write_text(project / "references.bib", "".join(parts).rstrip() + "\n")


def rewrite_inputs(body: str, root: Path, main_tex: Path) -> str:
    main_dir = main_tex.parent

    def normalize_safe_image(match: re.Match[str]) -> str:
        prefix, filename, suffix = match.groups()
        normalized = filename.replace("_", "-")
        if (
            not normalized.startswith(("figures/", "tables/", "imports/"))
            and Path(normalized).suffix.lower() in IMAGE_EXTS
        ):
            normalized = f"figures/{normalized}"
        return f"{prefix}{normalized}{suffix}"

    def repl(match: re.Match[str]) -> str:
        command = match.group(1)
        raw = match.group(2).strip()
        if raw.startswith("sections/"):
            return match.group(0)
        candidates = []
        raw_path = Path(raw)
        if raw_path.suffix:
            candidates.append(main_dir / raw_path)
            candidates.append(root / raw_path)
        else:
            candidates.append(main_dir / f"{raw}.tex")
            candidates.append(root / f"{raw}.tex")
        for candidate in candidates:
            if candidate.exists():
                rel = candidate.relative_to(root)
                without_suffix = (Path("sections") / rel).with_suffix("")
                return f"\\{command}" + "{" + without_suffix.as_posix() + "}"
        return match.group(0)

    pattern = re.compile(r"\\(input|include)\{([^}]+)\}")
    body = pattern.sub(repl, body)
    body = re.sub(r"\\bibliography\{[^}]+\}", r"\\bibliography{references}", body)
    body = re.sub(
        r"(\\safeincludegraphics\{[^}]+\}\{)([^}]+)(\})",
        normalize_safe_image,
        body,
    )
    return body


def normalize_preamble(preamble: str) -> str:
    preamble = re.sub(
        r"\\usepackage(?:\[[^]]+\])?\{newtxtext\}\s*\n?",
        "",
        preamble,
    )
    preamble = re.sub(
        r"\\usepackage(?:\[[^]]+\])?\{newtxmath\}\s*\n?",
        "",
        preamble,
    )
    preamble = re.sub(
        r"\\usepackage(?:\[[^]]+\])?\{helvet\}\s*\n?",
        "",
        preamble,
    )
    if "\\usepackage{fontspec}" not in preamble and "\\usepackage[no-math]{fontspec}" not in preamble:
        insert = (
            "\\usepackage{fontspec}\n"
            "\\setmainfont{TeX Gyre Termes}\n"
            "\\setsansfont{TeX Gyre Heros}\n"
        )
        documentclass = re.search(r"\\documentclass(?:\[[^]]+\])?\{[^}]+\}", preamble)
        if documentclass:
            idx = documentclass.end()
            preamble = preamble[:idx] + "\n" + insert + preamble[idx:]
        else:
            preamble = insert + preamble
    if "\\usepackage{microtype}" not in preamble:
        preamble = preamble.replace("\\usepackage{fontspec}", "\\usepackage{fontspec}\n\\usepackage{microtype}", 1)
    if "\\usepackage{graphicx}" not in preamble and "\\usepackage[pdftex]{graphicx}" not in preamble:
        preamble = preamble.replace("\\usepackage{microtype}", "\\usepackage{microtype}\n\\usepackage{graphicx}", 1)
    if "\\usepackage{amsmath,amssymb}" not in preamble and "\\usepackage{amssymb}" not in preamble:
        preamble = preamble.replace("\\usepackage{amsmath}", "\\usepackage{amsmath,amssymb}")
    if "\\emergencystretch" not in preamble:
        preamble += "\n\\emergencystretch=3em\n\\hbadness=10000\n"
    return preamble


def build_main_tex(preamble: str, body: str, source_name: str) -> str:
    preamble = normalize_preamble(preamble)
    graphicspath = "\\graphicspath{{./}{figures/}{figures/photo/}{tables/}{imports/original-source/}{imports/original-source/photo/}}"
    if "\\graphicspath" not in preamble:
        preamble = f"{preamble}\n\n{graphicspath}"
    else:
        preamble = re.sub(
            r"\\graphicspath\{(?:\{[^{}]*\})+\}",
            lambda _: graphicspath,
            preamble,
            count=1,
        )
    return f"""% Imported from {source_name} by scripts/import_latex_zip.py.
% Main LaTeX source is kept in this file. Additional .tex files, if any,
% are copied under sections/ and referenced from here.

{preamble}

\\begin{{document}}

{body}

\\end{{document}}
"""


def reset_import_dirs(project: Path) -> None:
    sections = project / "sections"
    if sections.exists():
        shutil.rmtree(sections)
    sections.mkdir(parents=True, exist_ok=True)


def import_zip(zip_path: Path, project: Path) -> None:
    if not zip_path.exists():
        raise SystemExit(f"Zip archive not found: {zip_path}")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = backup_existing(project, timestamp)

    with tempfile.TemporaryDirectory() as tmp:
        extracted = Path(tmp) / "extracted"
        extracted.mkdir()
        safe_extract(zip_path, extracted)
        root = source_root(extracted)
        main_tex = find_main_tex(root)
        all_tex = tex_files(root)
        raw_main = read_text(main_tex)
        preamble, body = split_document(raw_main)
        body = rewrite_inputs(body, root, main_tex)
        reset_import_dirs(project)

        original_source = project / "imports" / "original-source"
        if original_source.exists():
            shutil.rmtree(original_source)
        copy_tree_contents(root, original_source)
        copy_support_files(root, project, main_tex)
        merge_bibliography(root, project)

        write_text(project / "main.tex", build_main_tex(preamble, body, main_tex.name))

    print(f"Imported {zip_path} into {project}")
    print(f"Detected main file: {main_tex.relative_to(root)}")
    print(f"Detected .tex files: {len(all_tex)}")
    if len(all_tex) == 1:
        print("Single-tex import: the complete document was written to main.tex.")
    else:
        print("Multi-tex import: main document was written to main.tex; other .tex files were copied to sections/.")
    print(f"Backup written to: {backup_dir}")
    print("Next steps:")
    print("  make doctor")
    print("  make build")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert an existing LaTeX zip archive into this template layout."
    )
    parser.add_argument("zip", type=Path, help="Path to the existing LaTeX .zip archive")
    parser.add_argument(
        "--project",
        type=Path,
        default=Path.cwd(),
        help="Target project directory. Defaults to the current directory.",
    )
    args = parser.parse_args()
    import_zip(args.zip.resolve(), args.project.resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main())
