#!/bin/bash
set -e

PYTHON_VERSION="3.12.13"
VENV_DIR=".venv"

# Use system Python 3.12.13 or prompt to install if not found
if ! command -v python3.12 &> /dev/null; then
    echo "Python 3.12.13 not found. Please install it first."
    exit 1
fi

python3.12 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Environment setup complete. To activate: source $VENV_DIR/bin/activate"
