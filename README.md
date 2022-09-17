
# CAVE WEATHER DATA PULLER

This little tool pulls weather-related data from the EU CDS climate data service.

The tool pulls data related to the temperature, precipitation, water runoff, snow depth,
and evaporation from any given point on Earth. The accuracy of the data in the CDS service
is based on 27x27km grid data about weather, either measured or calculated. The data runs
from 1980s to present day.

There are two commands involved, one to pull data from the CDS servers
and another to process that data to a table that can be further
used. The usage of these commands are described below.

# PULL-DATA



    python3 pull-data.py [options] [ystart [yend]]

This pulls cave-relevant weather data from CDS. The argyument ystart
should be a four-digit year number to start the pulling from, and
the optional yend argument should another year to end the pulling
from. If yend is not provided, just the starting year is pulled. If
neither year value is provided, by default the command pulls just
the year 2019.

The command writes its output to a file data-ystart-yend.nc. If only
some months were selected, then the file name will end in either
program to print out the pulled data.

The pull-data.py command may also invoked with options:

    --month nn             Pull only month nn (expressed as a two-digit
                           month number)

    --months nn mm         Pull month nn to mm (expressed as a two-digit
                           month numbers)

    --coordinates lat lon  Use the coordinates 'lat' and 'lon'. By 
                           default the command uses the corodinates of
                           Njiellalanjävri in northern Finland.


# SHOW-DATA



    python3 show-data.py [options] [file.nc [anotherfile.nc ... ]]

The command reads data pulled earlier by pull-data.py into file file.nc.
It then proceeds to print the data in a convenient format. Options
are used to control what is printed, e.g., precipation, temperature, etc.

If no arguments are given, the file is assumed to be
data.nc. Several files can also be provided, in which case their
data is merged together. If no options are given, the software
behaves as if --combined option was specified, i.e., daily main
values are summarized from the input data.

The possible options are:

    --text             Use textual, human-readable output format. This is
                       the default.
    --csv              Use CSV (comma-separated-values) format for output.
    --full             Print everything in the original input tables
                       (for debugging etc)
    --combined         Print precipation, temperature, evaporation, snow
                       evaporation, runoff, and snow depth as daily values.
    --precipitation    Print data about precipitation, tabulated
                       as daily preciptation -- rain or snow --
                       in meters. For instance, 0.001 means 1mm
                       of rain.
    --temperature      Print data about temperature, as daily min,
                       avg, and max temperatures. Values are in C.
                       This is the default mode.
    --runoff           Print data about daily surface runoff. This
                       is in meters, 0.0001 means 1mm runoff.
    --runoffrate       Print data about average daily surface runoff
                       rate, i.e., kg / (m^2 s^1).
    --evaporation      Print data about daily evaporation. This is in
                       meters, 0.0001 means 1mm water equivalent
                       evaporation.
    --snowevaporation  Print data about daily evaporation of snow. This
                       is in meters, 0.0001 means 1mm water equivalent
                       evaporation.
    --snowdepth        Print data about snow depth. The depth is
                       represented by meters of water that the snow
                       covering the area would melt as, if the snow
                       were turned into water.
    --debug            Turn on debugging printouts.


