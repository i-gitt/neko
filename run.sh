#!/bin/sh

source venv/bin/activate
pip install -qr requirements.txt
python neko.py
