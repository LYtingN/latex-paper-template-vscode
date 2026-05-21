$ErrorActionPreference = "Stop"

function HasCommand($Name) {
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

if ((HasCommand "latexmk") -and (HasCommand "xelatex") -and (HasCommand "bibtex")) {
    Write-Host "LaTeX toolchain is already installed."
    latexmk -v | Select-Object -First 1
    xelatex --version | Select-Object -First 1
    exit 0
}

if (HasCommand "winget") {
    Write-Host "Installing MiKTeX with winget..."
    winget install --id MiKTeX.MiKTeX --exact --accept-package-agreements --accept-source-agreements
    Write-Host "Restart Cursor or the terminal, then run: make build"
    exit 0
}

if (HasCommand "choco") {
    Write-Host "Installing MiKTeX with Chocolatey..."
    choco install miktex -y
    Write-Host "Restart Cursor or the terminal, then run: make build"
    exit 0
}

Write-Error "No supported Windows package manager found. Install MiKTeX manually, then reopen Cursor."
