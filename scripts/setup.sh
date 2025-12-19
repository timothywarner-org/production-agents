#!/bin/bash
# =============================================================================
# setup.sh - One-command Python environment setup for macOS/Linux
# =============================================================================
# This script handles the tedious venv dance so you don't have to:
#   1. Creates a virtual environment (if it doesn't exist)
#   2. Activates it
#   3. Upgrades pip (avoids annoying warnings)
#   4. Installs dependencies in editable mode
#   5. Copies .env.example to .env (if needed)
#   6. Runs verification
#
# Usage:
#   chmod +x scripts/setup.sh   # Make executable (one time)
#   source scripts/setup.sh     # Run setup AND stay in the venv
#
# Why 'source' instead of './scripts/setup.sh'?
#   When you 'source' a script, it runs in your current shell, so the
#   virtual environment activation persists after the script ends.
#   Running it directly (./setup.sh) spawns a subshell that exits.
# =============================================================================

set -e  # Exit on any error

# Colors for output (makes it easier to follow)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the repository root (parent of scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$REPO_ROOT/.venv"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Production Agents - Environment Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# -----------------------------------------------------------------------------
# Step 1: Check Python version
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[1/6]${NC} Checking Python version..."

# Try python3 first (macOS/Linux convention), fall back to python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}ERROR: Python not found. Please install Python 3.11+${NC}"
    echo "  - macOS: brew install python@3.11"
    echo "  - Ubuntu: sudo apt install python3.11"
    exit 1
fi

# Verify version is 3.11+
PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
MAJOR_VERSION=$($PYTHON_CMD -c 'import sys; print(sys.version_info.major)')
MINOR_VERSION=$($PYTHON_CMD -c 'import sys; print(sys.version_info.minor)')

if [[ "$MAJOR_VERSION" -lt 3 ]] || [[ "$MAJOR_VERSION" -eq 3 && "$MINOR_VERSION" -lt 11 ]]; then
    echo -e "${RED}ERROR: Python 3.11+ required (found $PYTHON_VERSION)${NC}"
    echo "  Please install a newer version of Python."
    exit 1
fi

echo -e "  ${GREEN}Found Python $PYTHON_VERSION${NC}"

# -----------------------------------------------------------------------------
# Step 2: Create virtual environment
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[2/6]${NC} Setting up virtual environment..."

if [ -d "$VENV_DIR" ]; then
    echo -e "  ${GREEN}Virtual environment already exists at .venv/${NC}"
else
    echo "  Creating virtual environment..."
    $PYTHON_CMD -m venv "$VENV_DIR"
    echo -e "  ${GREEN}Created virtual environment at .venv/${NC}"
fi

# -----------------------------------------------------------------------------
# Step 3: Activate virtual environment
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[3/6]${NC} Activating virtual environment..."

# The magic: source the activate script
source "$VENV_DIR/bin/activate"

echo -e "  ${GREEN}Virtual environment activated${NC}"

# -----------------------------------------------------------------------------
# Step 4: Upgrade pip (prevents annoying warnings)
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[4/6]${NC} Upgrading pip..."

pip install --upgrade pip --quiet
echo -e "  ${GREEN}pip upgraded${NC}"

# -----------------------------------------------------------------------------
# Step 5: Install dependencies
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[5/6]${NC} Installing dependencies..."

# Install in editable mode - this makes the package importable AND
# lets you edit code without reinstalling
pip install -e "$REPO_ROOT" --quiet

# If you want dev dependencies too, uncomment:
# pip install -e "$REPO_ROOT[dev]" --quiet

echo -e "  ${GREEN}Dependencies installed${NC}"

# -----------------------------------------------------------------------------
# Step 6: Setup environment file
# -----------------------------------------------------------------------------
echo -e "${YELLOW}[6/6]${NC} Checking environment configuration..."

if [ ! -f "$REPO_ROOT/.env" ]; then
    if [ -f "$REPO_ROOT/.env.example" ]; then
        cp "$REPO_ROOT/.env.example" "$REPO_ROOT/.env"
        echo -e "  ${YELLOW}Created .env from .env.example${NC}"
        echo -e "  ${YELLOW}IMPORTANT: Edit .env and add your API keys!${NC}"
    else
        echo -e "  ${YELLOW}No .env.example found - skipping${NC}"
    fi
else
    echo -e "  ${GREEN}.env already exists${NC}"
fi

# -----------------------------------------------------------------------------
# Done!
# -----------------------------------------------------------------------------
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Setup complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Your virtual environment is now active."
echo ""
echo -e "Next steps:"
echo -e "  1. ${YELLOW}Edit .env${NC} and add your API keys"
echo -e "  2. ${YELLOW}python -m scripts.verify_setup${NC} to verify"
echo -e "  3. ${YELLOW}python -m segment_1_foundations.01_what_is_an_agent${NC} to start learning"
echo ""
echo -e "To deactivate the virtual environment later, type: ${BLUE}deactivate${NC}"
echo ""
