#!/bin/sh

python3 src/show-data.py --combined --text data-201?-201?.nc data-202?-202?.nc data-2022-2022-01-08.nc > combined-2016-2022.txt
python3 src/show-data.py --combined --csv data-201?-201?.nc data-202?-202?.nc data-2022-2022-01-08.nc > combined-2016-2022.csv
