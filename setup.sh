#!/usr/bin/env bash
chmod +x background-remover.py
python3 -m venv gimpenv
source gimpenv/bin/activate
python3 -m pip install numpy
python3 -m pip install pillow
python3 -m pip install torch
#python3 -m pip install torchvision
python3 -m pip install opencv-python
deactivate
