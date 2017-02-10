rm -r build
rm -r dist
python setup.py py2exe
cp -r examples dist
cp -r icons dist
mkdir dist/carbonxs
cp carbonxs/carbonxs_gfortran.exe dist/carbonxs
cp carbonxs/compiling.txt dist/carbonxs
cp carbonxs/CARBONXS.FOR dist/carbonxs
cp carbonxs/carbon.cmn dist/carbonxs
cp -r docs dist
cp -r config dist
cp -r README.md dist
cp winlib/*.dll dist/carbonxs



