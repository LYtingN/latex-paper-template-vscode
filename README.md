# LaTeX Paper Template Starter

English | [中文](#中文说明)

A clean LaTeX paper starter for Cursor, VS Code, and Codex-assisted writing. It
uses `latexmk + XeLaTeX`, keeps all generated files under `build/`, and includes
helpers for local diagnosis, GitHub Actions builds, and importing an existing
LaTeX zip project.

## What You Get

- Minimal paper skeleton in `main.tex`
- Section-based writing under `sections/`
- Empty `figures/` and `tables/` asset folders
- `latexmkrc` configured for XeLaTeX output in `build/`
- Cursor/VS Code LaTeX Workshop settings
- `make doctor` project check and PDF build
- Optional Codex skill installer for LaTeX build repair
- GitHub Actions workflow that builds and uploads `build/main.pdf`

## Quick Start

Open this folder as the project root:

```bash
cd /path/to/latex-paper-template-starter
```

Check the toolchain and build the PDF:

```bash
make doctor
```

The generated PDF is:

```text
build/main.pdf
```

If LaTeX tools are missing, run:

```bash
make setup
```

On Windows PowerShell:

```powershell
.\scripts\setup.ps1
make doctor
```

## Writing Workflow

Edit these files first:

- `main.tex`: title, author, metadata, section order
- `sections/*.tex`: paper content
- `references.bib`: bibliography entries
- `figures/`: images
- `tables/`: table data or exported assets

For continuous local rebuilds:

```bash
make watch
```

To clean generated files:

```bash
make clean
make distclean
```

## Cursor / VS Code Preview

1. Open this folder directly, not only its parent workspace.
2. Install the recommended extension: `LaTeX Workshop`.
3. Open `main.tex`.
4. Save with `Ctrl+S` / `Cmd+S`.
5. Run `LaTeX Workshop: View LaTeX PDF file`.
6. Use the PDF opened by LaTeX Workshop, not a manually opened root-level PDF.

This template is configured to build with XeLaTeX. If you see `pdflatex` or
`lualatex` in the build log, switch the recipe to `latexmk (fast xelatex)` or
run `make doctor` from the terminal.

## Commands

```bash
make check         # Check whether latexmk and xelatex are installed
make doctor        # Validate structure and build build/main.pdf
make build         # Build build/main.pdf
make watch         # Rebuild automatically when files change
make clean         # Remove LaTeX auxiliary files
make distclean     # Remove build/ and generated files
make import-zip ZIP=/path/to/project.zip
make install-skill # Install the bundled Codex latex-doctor-fix skill
```

## Project Layout

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
└── .github/workflows/latex.yml
```

Generated output belongs in `build/`. Do not edit `build/` files directly.

## Codex Skill

The repository includes an installable Codex skill:

```text
codex-skills/latex-doctor-fix
```

Install it with:

```bash
make install-skill
```

After starting a new Codex session, you can ask:

```text
Use $latex-doctor-fix to run make doctor and fix the LaTeX build problem.
```

## Import an Existing Paper

To migrate an existing LaTeX zip:

```bash
make import-zip ZIP=/path/to/your-paper.zip
make doctor
```

The importer detects the main `.tex` file, copies figures and tables into the
template layout, rewrites common `\input{...}` paths, merges `.bib` files into
`references.bib`, and stores the original source under `imports/original-source/`.

Review the imported `main.tex` and `sections/` files before continuing.

## GitHub Actions

`.github/workflows/latex.yml` runs on `push` and `pull_request`.

It installs a TeX Live toolchain, runs:

```bash
make doctor
```

and uploads:

```text
build/main.pdf
```

as a workflow artifact. This confirms that the repository builds on a clean
Ubuntu machine, not only on your local computer.

## Troubleshooting

If the PDF does not update after saving:

- Make sure `main.tex` is the active editor when you press `Ctrl+S`.
- Open the PDF through `LaTeX Workshop: View LaTeX PDF file`.
- Check `View -> Output -> LaTeX Workshop`.
- Run `make doctor` and fix the first reported failure.

If root-level files like `main.aux`, `main.log`, or `main.pdf` appear, your
editor probably bypassed `latexmkrc`. Delete those generated files and build
with `make doctor` or the `latexmk (fast xelatex)` recipe.

## Before Publishing

Update:

- `README.md` project name and description
- `main.tex` title, author, and PDF metadata
- `references.bib`
- repository license file, if you want to publish the template or paper

---

# 中文说明

[English](#latex-paper-template-starter) | 中文

这是一个干净的 LaTeX 论文模板，适合在 Cursor、VS Code 和 Codex 中写作。它默认使用
`latexmk + XeLaTeX`，所有编译输出都放在 `build/`，并包含本地诊断、GitHub Actions
自动构建和 Codex 修复 skill。

## 包含内容

- `main.tex` 最小论文入口
- `sections/` 分章节写作结构
- 空的 `figures/` 和 `tables/` 资源目录
- 使用 XeLaTeX 的 `latexmkrc`
- Cursor/VS Code LaTeX Workshop 配置
- `make doctor` 检查项目并构建 PDF
- 可选安装的 Codex `latex-doctor-fix` skill
- GitHub Actions 自动构建并上传 `build/main.pdf`

## 快速开始

进入项目根目录：

```bash
cd /path/to/latex-paper-template-starter
```

检查并构建：

```bash
make doctor
```

PDF 输出位置：

```text
build/main.pdf
```

如果缺少 LaTeX 工具：

```bash
make setup
```

Windows PowerShell:

```powershell
.\scripts\setup.ps1
make doctor
```

## 写作流程

优先编辑：

- `main.tex`：标题、作者、metadata、章节顺序
- `sections/*.tex`：正文
- `references.bib`：参考文献
- `figures/`：图片
- `tables/`：表格或数据文件

持续监听并自动编译：

```bash
make watch
```

清理生成文件：

```bash
make clean
make distclean
```

## Cursor / VS Code 预览

1. 直接打开本目录，不要只打开外层工作区。
2. 安装推荐扩展：`LaTeX Workshop`。
3. 打开 `main.tex`。
4. 按 `Ctrl+S` / `Cmd+S` 保存。
5. 运行 `LaTeX Workshop: View LaTeX PDF file`。
6. 使用 LaTeX Workshop 打开的 PDF，不要手动打开根目录下的旧 PDF。

本模板必须用 XeLaTeX。如果日志里出现 `pdflatex` 或 `lualatex`，请切换到
`latexmk (fast xelatex)` recipe，或直接在终端运行 `make doctor`。

## 常用命令

```bash
make check         # 检查 latexmk 和 xelatex 是否安装
make doctor        # 检查项目结构并构建 build/main.pdf
make build         # 构建 build/main.pdf
make watch         # 文件变化时自动重新构建
make clean         # 删除 LaTeX 辅助文件
make distclean     # 删除 build/ 和生成文件
make import-zip ZIP=/path/to/project.zip
make install-skill # 安装随仓库提供的 Codex latex-doctor-fix skill
```

## Codex Skill

仓库自带可安装的 Codex skill：

```text
codex-skills/latex-doctor-fix
```

安装：

```bash
make install-skill
```

新开 Codex 会话后可以使用：

```text
Use $latex-doctor-fix to run make doctor and fix the LaTeX build problem.
```

## GitHub Actions

`.github/workflows/latex.yml` 会在 `push` 和 `pull_request` 时运行。

它会安装 TeX Live，执行：

```bash
make doctor
```

并把生成的 PDF 上传为 artifact：

```text
build/main.pdf
```

这样可以确认仓库在一台干净的 Ubuntu 机器上也能成功编译。

## 故障排查

如果保存后 PDF 没更新：

- 确认按 `Ctrl+S` 时焦点在 `main.tex` 编辑器里。
- 用 `LaTeX Workshop: View LaTeX PDF file` 打开 PDF。
- 查看 `View -> Output -> LaTeX Workshop`。
- 运行 `make doctor`，优先修复第一个失败点。

如果根目录出现 `main.aux`、`main.log` 或 `main.pdf`，说明编辑器绕过了
`latexmkrc`。删除这些生成文件，然后用 `make doctor` 或 `latexmk (fast xelatex)`
重新构建。

## 发布前检查

发布前请更新：

- `README.md` 项目名称和描述
- `main.tex` 标题、作者和 PDF metadata
- `references.bib`
- 如果要开源，请添加或更新仓库 license 文件
