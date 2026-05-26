#!/usr/bin/env bash
set -euo pipefail

# Creates a Python virtual environment in ./venv and installs requirements
python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Virtual environment created and packages installed. Activate with: source venv/bin/activate"
echo "The notebook loads the local slurm_magic.py file directly."
echo "If you need RISE for in-notebook slides: pip install RISE" 