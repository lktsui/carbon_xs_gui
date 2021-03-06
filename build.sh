#!/usr/bin/env bash
rm -r build
rm -r dist
python setup.py py2exe
cp -r examples dist
cp -r icons dist
cp -r fonts dist
mkdir dist/carbonxs
cp carbonxs/carbonxs_gfortran.exe dist/carbonxs
cp carbonxs/compiling.txt dist/carbonxs
cp carbonxs/CARBONXS.FOR dist/carbonxs
cp carbonxs/carbon.cmn dist/carbonxs
cp -r docs dist
cp -r config dist
cp -r README.md dist
cp LICENSE dist
cp winlib/*.dll dist/carbonxs
git archive master --format zip -o dist/src.zip
rm dist.zip
7z a dist.zip ./dist/*
mv dist.zip versions/dist_$(date +%F-%H%M).zip