#!/usr/bin/env sh
chmod +x build.sh
rm -rf dist build
pip install -r requirements.txt
python3 setup.py py2app --includes --packages
