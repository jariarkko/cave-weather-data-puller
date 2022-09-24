#
# Run this script to install all the tooling needed for using the CDS
# service in Python.
#
# You will also have to register as a user of the CDS service, and
# install your API key two-liner at .cdsapirc in your home directory.
#
# The script is made for Mac OS but can probably be modified easily to
# run on Linux as well.
#

HDF5_DIR=/opt/homebrew/Cellar/hdf5/1.12.2_1
export HDF5_DIR
brew install netcdf HDF5
pip3 install --upgrade pip
pip3 install numpy
pip3 install cdsapi
pip3 install netCDF4
pip3 install matplotlib
pip3 install pandas
pip3 install tabulate
pip3 install seaborn
