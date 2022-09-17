#!/bin/sh

COMMANDSCRIPT=$0
AWKSCRIPT=`echo $COMMANDSCRIPT | sed 's/[.]sh/.awk/'`
PULLSCRIPT=`echo $COMMANDSCRIPT | sed 's%readusage[.]sh%../src/pull-data.py%'`
SHOWSCRIPT=`echo $COMMANDSCRIPT | sed 's%readusage[.]sh%../src/show-data.py%'`

echo ""
echo "# cave-weather-data-puller"
echo ""
echo "This little tool pulls weather-related data from the EU CDS climate data service."
echo ""
echo "The tool pulls data related to the temperature, precipitation, water runoff, snow depth,"
echo "and evaporation from any given point on Earth. The accuracy of the data in the CDS service"
echo "is based on 27x27km grid data about weather, either measured or calculated. The data runs"
echo "from 1980s to present day."
echo ""
echo "There are two commands involved, one to pull data from the CDS servers"
echo "and another to process that data to a table that can be further"
echo "used. The usage of these commands are described below."
echo ""
echo "# PULL-DATA"
echo ""
awk -f $AWKSCRIPT < $PULLSCRIPT
echo ""
echo "# SHOW-DATA"
echo ""
awk -f $AWKSCRIPT < $SHOWSCRIPT
echo ""

