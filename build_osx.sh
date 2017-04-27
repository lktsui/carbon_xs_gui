#!/usr/bin/env bash
rm -rf build
rm -rf dist
pyinstaller -w carbonxs_pyinstaller_osx.spec
mkdir dist/CarbonXS_GUI.app/Contents/MacOs/carbonxs
mkdir dist/CarbonXS_GUI.app/Contents/MacOs/config
mkdir dist/CarbonXS_GUI.app/Contents/MacOs/fonts
cp -r config/fitting\ settings dist/CarbonXS_GUI.app/Contents/MacOs/config
cp -r config/fitting\ parameters dist/CarbonXS_GUI.app/Contents/MacOs/config
cp -r config/diffractometer\ settings dist/CarbonXS_GUI.app/Contents/MacOs/config
cp -r examples dist/CarbonXS_GUI.app/Contents/MacOs/
cp carbonxs/carbonxs_app dist/CarbonXS_GUI.app/Contents/MacOs/carbonxs
cp carbonxs/carbon.inp dist/CarbonXS_GUI.app/Contents/MacOs/carbonxs
cp fonts/SourceCodePro-Regular.ttf dist/CarbonXS_GUI.app/Contents/MacOs/fonts
cp fonts/OFL.txt dist/CarbonXS_GUI.app/Contents/MacOs/fonts
cp -r icons dist/CarbonXS_GUI.app/Contents/MacOs/
timestamp=`date +%Y%m%d-%H%M`
osx_version=`sw_vers -productVersion`
folder=build_osx${osx_version}_${timestamp}
mkdir dist/$folder
mv dist/CarbonXS_GUI.app dist/$folder/CarbonXS_GUI.app