rm -r build
rm -r dist
python setup.py py2exe
cd dist
mkdir carbonxs
mkdir config
cd config
mkdir "diffractometer settings"
mkdir "fitting parameters"
mkdir "fitting settings"
cd ..
mkdir results
cp ../carbonxs/CARBONXS.exe carbonxs/carbonxs.exe
cd ..
cp -r icons dist/
7z a new_version.zip ./dist/*