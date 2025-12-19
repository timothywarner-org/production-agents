# =============================================================================
# setup.ps1 - One-command Python environment setup for Windows PowerShell
# =============================================================================
# This script handles the tedious venv dance so you don't have to:
#   1. Creates a virtual environment (if it doesn't exist)
#   2. Activates it
#   3. Upgrades pip (avoids annoying warnings)
#   4. Installs dependencies in editable mode
#   5. Copies .env.example to .env (if needed)
#   6. Runs verification
#
# Usage (PowerShell):
#   .\scripts\setup.ps1
#
# If you get an execution policy error, run this first (as Administrator):
#   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
#
# Why this script?
#   Tim Warner gets "squirrely" with Python venvs (his words). This script
#   eliminates the cognitive overhead of remembering activation commands
#   and the correct order of operations.
# =============================================================================

$ErrorActionPreference = "Stop"

# Colors for output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

# Get the repository root (parent of scripts/)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$VenvDir = Join-Path $RepoRoot ".venv"

Write-Host ""
Write-Host "========================================" -ForegroundColor Blue
Write-Host "  Production Agents - Environment Setup" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""

# -----------------------------------------------------------------------------
# Step 1: Check Python version
# -----------------------------------------------------------------------------
Write-Host "[1/6] Checking Python version..." -ForegroundColor Yellow

# Try to find Python
$PythonCmd = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $version = & $cmd --version 2>&1
        if ($version -match "Python (\d+)\.(\d+)") {
            $PythonCmd = $cmd
            break
        }
    } catch {
        # Command not found, try next
    }
}

if (-not $PythonCmd) {
    Write-Host "ERROR: Python not found. Please install Python 3.11+" -ForegroundColor Red
    Write-Host "  Download from: https://www.python.org/downloads/"
    Write-Host "  Or via winget: winget install Python.Python.3.11"
    exit 1
}

# Verify version is 3.11+
$VersionOutput = & $PythonCmd -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
$MajorVersion = & $PythonCmd -c "import sys; print(sys.version_info.major)"
$MinorVersion = & $PythonCmd -c "import sys; print(sys.version_info.minor)"

if (([int]$MajorVersion -lt 3) -or (([int]$MajorVersion -eq 3) -and ([int]$MinorVersion -lt 11))) {
    Write-Host "ERROR: Python 3.11+ required (found $VersionOutput)" -ForegroundColor Red
    Write-Host "  Please install a newer version of Python."
    exit 1
}

Write-Host "  Found Python $VersionOutput" -ForegroundColor Green

# -----------------------------------------------------------------------------
# Step 2: Create virtual environment
# -----------------------------------------------------------------------------
Write-Host "[2/6] Setting up virtual environment..." -ForegroundColor Yellow

if (Test-Path $VenvDir) {
    Write-Host "  Virtual environment already exists at .venv\" -ForegroundColor Green
} else {
    Write-Host "  Creating virtual environment..."
    & $PythonCmd -m venv $VenvDir
    Write-Host "  Created virtual environment at .venv\" -ForegroundColor Green
}

# -----------------------------------------------------------------------------
# Step 3: Activate virtual environment
# -----------------------------------------------------------------------------
Write-Host "[3/6] Activating virtual environment..." -ForegroundColor Yellow

$ActivateScript = Join-Path $VenvDir "Scripts\Activate.ps1"
if (-not (Test-Path $ActivateScript)) {
    Write-Host "ERROR: Activation script not found at $ActivateScript" -ForegroundColor Red
    exit 1
}

# Activate the virtual environment
. $ActivateScript

Write-Host "  Virtual environment activated" -ForegroundColor Green

# -----------------------------------------------------------------------------
# Step 4: Upgrade pip (prevents annoying warnings)
# -----------------------------------------------------------------------------
Write-Host "[4/6] Upgrading pip..." -ForegroundColor Yellow

& pip install --upgrade pip --quiet
Write-Host "  pip upgraded" -ForegroundColor Green

# -----------------------------------------------------------------------------
# Step 5: Install dependencies
# -----------------------------------------------------------------------------
Write-Host "[5/6] Installing dependencies..." -ForegroundColor Yellow

# Install in editable mode - this makes the package importable AND
# lets you edit code without reinstalling
& pip install -e $RepoRoot --quiet

# If you want dev dependencies too, uncomment:
# & pip install -e "$RepoRoot[dev]" --quiet

Write-Host "  Dependencies installed" -ForegroundColor Green

# -----------------------------------------------------------------------------
# Step 6: Setup environment file
# -----------------------------------------------------------------------------
Write-Host "[6/6] Checking environment configuration..." -ForegroundColor Yellow

$EnvFile = Join-Path $RepoRoot ".env"
$EnvExample = Join-Path $RepoRoot ".env.example"

if (-not (Test-Path $EnvFile)) {
    if (Test-Path $EnvExample) {
        Copy-Item $EnvExample $EnvFile
        Write-Host "  Created .env from .env.example" -ForegroundColor Yellow
        Write-Host "  IMPORTANT: Edit .env and add your API keys!" -ForegroundColor Yellow
    } else {
        Write-Host "  No .env.example found - skipping" -ForegroundColor Yellow
    }
} else {
    Write-Host "  .env already exists" -ForegroundColor Green
}

# -----------------------------------------------------------------------------
# Done!
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Setup complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your virtual environment is now active."
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. " -NoNewline; Write-Host "Edit .env" -ForegroundColor Yellow -NoNewline; Write-Host " and add your API keys"
Write-Host "  2. " -NoNewline; Write-Host "python -m scripts.verify_setup" -ForegroundColor Yellow -NoNewline; Write-Host " to verify"
Write-Host "  3. " -NoNewline; Write-Host "python -m segment_1_foundations.01_what_is_an_agent" -ForegroundColor Yellow -NoNewline; Write-Host " to start learning"
Write-Host ""
Write-Host "To deactivate the virtual environment later, type: " -NoNewline; Write-Host "deactivate" -ForegroundColor Blue
Write-Host ""
