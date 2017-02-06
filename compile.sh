cd carbonxs
echo "Attempting to Compile CarbonXS"
gfortran CARBONXS.FOR -fno-automatic -static-libgcc -std=legacy -O3 -o carbonxs_app
echo "Compilation attempt completed"
cd ..
