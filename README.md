# LaTeX Paper Template Starter

English | [中文](#中文说明)

A clean LaTeX paper template for Cursor, VS Code, and Codex-assisted writing.
It builds with `latexmk + XeLaTeX` and writes generated files to `build/`.

## Quick Start

Open this directory as the project root:

```bash
cd /path/to/latex-paper-template-starter
```

First-time setup:

```bash
make init
```

Everyday writing build:

```bash
make build
```

Before committing, sharing, or debugging:

```bash
make doctor
```

PDF output:

```text
build/main.pdf
```

## Which Command Should I Use?

| Task | Command |
| --- | --- |
| Install tools and build once | `make init` |
| Build the PDF | `make build` |
| Watch files and rebuild automatically | `make watch` |
| Check structure and build health | `make doctor` |
| Check installed LaTeX tools | `make check` |
| Remove auxiliary files | `make clean` |
| Remove `build/` completely | `make distclean` |
| Import a zipped LaTeX project | `make import-zip ZIP=/path/to/project.zip` |
| Install the bundled Codex skill | `make install-skill` |

## Project Structure

```text
.
├── main.tex                  # Document entry point
├── references.bib            # Bibliography database
├── sections/                 # Paper sections
├── figures/                  # Figure assets
├── tables/                   # Table/data assets
├── latexmkrc                 # XeLaTeX build configuration
├── Makefile                  # Common commands
├── scripts/                  # Setup/import/skill scripts
├── codex-skills/             # Bundled Codex skill
├── .vscode/                  # VS Code/Cursor settings
├── .cursor/rules/            # Cursor agent rules
└── .github/workflows/        # GitHub Actions build check
```

Edit `main.tex`, `sections/*.tex`, `references.bib`, `figures/`, and `tables/`.
Do not edit `build/` or LaTeX auxiliary files.

## Cursor / VS Code

1. Open this folder directly, not only its parent folder.
2. Install the recommended extension: `LaTeX Workshop`.
3. Open `main.tex`.
4. Save with `Ctrl+S` / `Cmd+S`.
5. Open the preview with `LaTeX Workshop: View LaTeX PDF file`.

The configured recipe is `latexmk (fast xelatex)`. If the log shows `pdflatex`
or `lualatex`, switch back to that recipe or run `make build` in the terminal.

## Codex Skill

This repo bundles:

```text
codex-skills/latex-doctor-fix
```

Install it with:

```bash
make install-skill
```

Then start a new Codex session and ask:

```text
Use $latex-doctor-fix to run make doctor and fix the LaTeX build problem.
```

## Import Existing LaTeX

```bash
make import-zip ZIP=/path/to/your-paper.zip
make doctor
```

The importer copies figures/tables, rewrites common `\input{...}` paths, merges
`.bib` files, and preserves the original source under `imports/original-source/`.
Review imported files before editing further.

## GitHub Actions

`.github/workflows/latex.yml` runs on `push` and `pull_request`.

It installs TeX Live, runs:

```bash
make doctor
```

and uploads `build/main.pdf` as an artifact. This verifies the paper on a clean
Ubuntu runner.

## Troubleshooting

If the PDF does not update:

- Make sure `main.tex` is the active editor when saving.
- Open the PDF through LaTeX Workshop, not the file manager.
- Check `View -> Output -> LaTeX Workshop`.
- Run `make doctor` and fix the first failure.

If root-level files such as `main.aux`, `main.log`, or `main.pdf` appear, your
editor bypassed `latexmkrc`. Delete those generated files and build with
`make build` or the `latexmk (fast xelatex)` recipe.

## Before Publishing

Update the title, author, PDF metadata, references, README description, and
license information for your own project.

---

# 中文说明

[English](#latex-paper-template-starter) | 中文

这是一个干净的 LaTeX 论文模板，适合 Cursor、VS Code 和 Codex 辅助写作。默认使用
`latexmk + XeLaTeX`，所有生成文件写入 `build/`。

## 快速开始

进入项目根目录：

```bash
cd /path/to/latex-paper-template-starter
```

首次使用：

```bash
make init
```

日常写作构建：

```bash
make build
```

提交、分享或排查问题前：

```bash
make doctor
```

PDF 输出：

```text
build/main.pdf
```

## 命令选择

| 任务 | 命令 |
| --- | --- |
| 安装工具并构建一次 | `make init` |
| 构建 PDF | `make build` |
| 监听文件并自动构建 | `make watch` |
| 检查结构和构建状态 | `make doctor` |
| 检查 LaTeX 工具链 | `make check` |
| 删除辅助文件 | `make clean` |
| 删除整个 `build/` | `make distclean` |
| 导入 LaTeX zip 项目 | `make import-zip ZIP=/path/to/project.zip` |
| 安装内置 Codex skill | `make install-skill` |

## 项目结构

```text
.
├── main.tex
├── references.bib
├── sections/
├── figures/
├── tables/
├── latexmkrc
├── Makefile
├── scripts/
├── codex-skills/
├── .vscode/
├── .cursor/rules/
└── .github/workflows/
```

只编辑 `main.tex`、`sections/*.tex`、`references.bib`、`figures/` 和 `tables/`。
不要编辑 `build/` 或 LaTeX 辅助文件。

## Cursor / VS Code

1. 直接打开本文件夹，不要只打开上一级目录。
2. 安装推荐扩展：`LaTeX Workshop`。
3. 打开 `main.tex`。
4. 按 `Ctrl+S` / `Cmd+S` 保存。
5. 用 `LaTeX Workshop: View LaTeX PDF file` 打开预览。

默认 recipe 是 `latexmk (fast xelatex)`。如果日志里出现 `pdflatex` 或
`lualatex`，切回该 recipe，或在终端运行 `make build`。

## Codex Skill

仓库内置：

```text
codex-skills/latex-doctor-fix
```

安装：

```bash
make install-skill
```

新开 Codex 会话后使用：

```text
Use $latex-doctor-fix to run make doctor and fix the LaTeX build problem.
```

## 导入已有 LaTeX 项目

```bash
make import-zip ZIP=/path/to/your-paper.zip
make doctor
```

导入器会复制图片和表格、改写常见 `\input{...}` 路径、合并 `.bib` 文件，并把原始
源码保存在 `imports/original-source/`。导入后先检查文件，再继续写作。

## GitHub Actions

`.github/workflows/latex.yml` 会在 `push` 和 `pull_request` 时运行。

它会安装 TeX Live，执行：

```bash
make doctor
```

并上传 `build/main.pdf`。这能确认仓库在干净的 Ubuntu 环境中也能编译。

## 故障排查

如果 PDF 没更新：

- 保存时确认焦点在 `main.tex`。
- 用 LaTeX Workshop 打开 PDF，不要用文件管理器手动打开。
- 查看 `View -> Output -> LaTeX Workshop`。
- 运行 `make doctor`，修复第一个失败点。

如果根目录出现 `main.aux`、`main.log` 或 `main.pdf`，说明编辑器绕过了
`latexmkrc`。删除这些生成文件，用 `make build` 或 `latexmk (fast xelatex)` 重建。

## 发布前

更新标题、作者、PDF metadata、参考文献、README 描述和 license 信息。
