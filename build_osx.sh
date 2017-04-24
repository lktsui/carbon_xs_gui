#!/usr/bin/env bash
rm -rf build
rm -rf dist
deactivate
source csx_venv/bin/activate
pyinstaller -w CarbonXS_GUI.py
mkdir dist/CarbonXS_GUI.app/Contents/MacOs/carbonxs
mkdir dist/CarbonXS_GUI.app/Contents/MacOs/config
mkdir dist/CarbonXS_GUI.app/Contents/MacOs/fonts
cp carbonxs/carbonxs_app dist/CarbonXS_GUI.app/Contents/MacOs/carbonxs
cp carbonxs/carbon.inp dist/CarbonXS_GUI.app/Contents/MacOs/carbonxs
cp fonts/SourceCodePro-Regular.ttf dist/CarbonXS_GUI.app/Contents/MacOs/fonts
cp fonts/OFL.txt dist/CarbonXS_GUI.app/Contents/MacOs/fonts
cp -r icons dist/CarbonXS_GUI.app/Contents/MacOs/
