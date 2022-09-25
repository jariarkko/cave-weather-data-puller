#!/bin/sh

for y in 2015 2016 2017 2018 2019 2020 2021
do
    python3 src/pull-data.py $y
done

python3 src/pull-data.py --months 01 08 2022
