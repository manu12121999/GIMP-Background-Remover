#!/usr/bin/env bash

# MAKE SCRIPT EXECUTABLE
chmod +x background-remover.py

# INSTALL DEPENDENCIES
python3 -m venv gimpenv
source gimpenv/bin/activate

python3 -m pip install numpy
python3 -m pip install pillow
python3 -m pip install torch==2.5 --index-url https://download.pytorch.org/whl/cpu
#python3 -m pip install torchvision
python3 -m pip install opencv-python
deactivate


# CHECK IF THE FOLDER NAMES ARE CORRECT
SCRIPT_PATH="$(realpath "$0")"

# Get the parent and grandparent folder names
PARENT_DIR=$(basename "$(dirname "$SCRIPT_PATH")")
GRANDPARENT_DIR=$(basename "$(dirname "$(dirname "$SCRIPT_PATH")")")

# Check if the folder names match
if [[ "$PARENT_DIR" != "background-remover" ]]; then
    echo "CHECK YOUR PATHS: THE .PY FILE SHOULD BE PLACED IN A FOLDER OF THE SAME NAME, e.g. 'background-remover.py' inside 'background-remover'."
fi

if [[ "$GRANDPARENT_DIR" != "plug-ins" ]]; then
    echo "THE GRANDPARENT FOLDER OF THE SCRIPT SHOULD BE 'plug-ins'. FOUND: $GRANDPARENT_DIR"
fi