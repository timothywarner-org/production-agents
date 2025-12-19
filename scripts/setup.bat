@echo off
REM =============================================================================
REM setup.bat - One-command Python environment setup for Windows Command Prompt
REM =============================================================================
REM This script handles the tedious venv dance so you don't have to:
REM   1. Creates a virtual environment (if it doesn't exist)
REM   2. Activates it
REM   3. Upgrades pip (avoids annoying warnings)
REM   4. Installs dependencies in editable mode
REM   5. Copies .env.example to .env (if needed)
REM
REM Usage (Command Prompt):
REM   scripts\setup.bat
REM
REM Why this script?
REM   Tim Warner gets "squirrely" with Python venvs (his words). This script
REM   eliminates the cognitive overhead of remembering activation commands
REM   and the correct order of operations.
REM =============================================================================

setlocal enabledelayedexpansion

REM Get the repository root (parent of scripts\)
set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%.."
cd /d "%REPO_ROOT%"
set "REPO_ROOT=%CD%"
set "VENV_DIR=%REPO_ROOT%\.venv"

echo.
echo ========================================
echo   Production Agents - Environment Setup
echo ========================================
echo.

REM -----------------------------------------------------------------------------
REM Step 1: Check Python version
REM -----------------------------------------------------------------------------
echo [1/6] Checking Python version...

REM Try to find Python
set "PYTHON_CMD="
where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PYTHON_CMD=python"
) else (
    where python3 >nul 2>nul
    if %errorlevel% equ 0 (
        set "PYTHON_CMD=python3"
    ) else (
        where py >nul 2>nul
        if %errorlevel% equ 0 (
            set "PYTHON_CMD=py"
        )
    )
)

if "%PYTHON_CMD%"=="" (
    echo ERROR: Python not found. Please install Python 3.11+
    echo   Download from: https://www.python.org/downloads/
    echo   Or via winget: winget install Python.Python.3.11
    exit /b 1
)

REM Verify version is 3.11+
for /f "tokens=*" %%i in ('%PYTHON_CMD% -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"') do set PYTHON_VERSION=%%i
for /f "tokens=*" %%i in ('%PYTHON_CMD% -c "import sys; print(sys.version_info.major)"') do set MAJOR_VERSION=%%i
for /f "tokens=*" %%i in ('%PYTHON_CMD% -c "import sys; print(sys.version_info.minor)"') do set MINOR_VERSION=%%i

if %MAJOR_VERSION% lss 3 (
    echo ERROR: Python 3.11+ required ^(found %PYTHON_VERSION%^)
    exit /b 1
)
if %MAJOR_VERSION% equ 3 if %MINOR_VERSION% lss 11 (
    echo ERROR: Python 3.11+ required ^(found %PYTHON_VERSION%^)
    exit /b 1
)

echo   Found Python %PYTHON_VERSION%

REM -----------------------------------------------------------------------------
REM Step 2: Create virtual environment
REM -----------------------------------------------------------------------------
echo [2/6] Setting up virtual environment...

if exist "%VENV_DIR%" (
    echo   Virtual environment already exists at .venv\
) else (
    echo   Creating virtual environment...
    %PYTHON_CMD% -m venv "%VENV_DIR%"
    echo   Created virtual environment at .venv\
)

REM -----------------------------------------------------------------------------
REM Step 3: Activate virtual environment
REM -----------------------------------------------------------------------------
echo [3/6] Activating virtual environment...

call "%VENV_DIR%\Scripts\activate.bat"
echo   Virtual environment activated

REM -----------------------------------------------------------------------------
REM Step 4: Upgrade pip (prevents annoying warnings)
REM -----------------------------------------------------------------------------
echo [4/6] Upgrading pip...

pip install --upgrade pip --quiet
echo   pip upgraded

REM -----------------------------------------------------------------------------
REM Step 5: Install dependencies
REM -----------------------------------------------------------------------------
echo [5/6] Installing dependencies...

REM Install in editable mode - this makes the package importable AND
REM lets you edit code without reinstalling
pip install -e "%REPO_ROOT%" --quiet
echo   Dependencies installed

REM -----------------------------------------------------------------------------
REM Step 6: Setup environment file
REM -----------------------------------------------------------------------------
echo [6/6] Checking environment configuration...

if not exist "%REPO_ROOT%\.env" (
    if exist "%REPO_ROOT%\.env.example" (
        copy "%REPO_ROOT%\.env.example" "%REPO_ROOT%\.env" >nul
        echo   Created .env from .env.example
        echo   IMPORTANT: Edit .env and add your API keys!
    ) else (
        echo   No .env.example found - skipping
    )
) else (
    echo   .env already exists
)

REM -----------------------------------------------------------------------------
REM Done!
REM -----------------------------------------------------------------------------
echo.
echo ========================================
echo   Setup complete!
echo ========================================
echo.
echo Your virtual environment is now active.
echo.
echo Next steps:
echo   1. Edit .env and add your API keys
echo   2. python -m scripts.verify_setup to verify
echo   3. python -m segment_1_foundations.01_what_is_an_agent to start learning
echo.
echo To deactivate the virtual environment later, type: deactivate
echo.

REM Keep the environment active for the user
endlocal & call "%VENV_DIR%\Scripts\activate.bat"
