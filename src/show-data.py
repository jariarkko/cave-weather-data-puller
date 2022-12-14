#
# Call as follows
#
#   python3 show-data.py [options] [file.nc [anotherfile.nc ... ]]
#
# The command reads data pulled earlier by pull-data.py into file file.nc.
# It then proceeds to print the data in a convenient format. Options
# are used to control what is printed, e.g., precipation, temperature, etc.
#
# If no arguments are given, the file is assumed to be
# data.nc. Several files can also be provided, in which case their
# data is merged together. If no options are given, the software
# behaves as if --combined option was specified, i.e., daily main
# values are summarized from the input data.
#
# The possible options are:
#
#   --text             Use textual, human-readable output format. This is
#                      the default.
#   --csv              Use CSV (comma-separated-values) format for output.
#   --full             Print everything in the original input tables
#                      (for debugging etc)
#   --combined         Print precipation, temperature, evaporation, snow
#                      evaporation, runoff, and snow depth as daily values.
#   --precipitation    Print data about precipitation, tabulated
#                      as daily preciptation -- rain or snow --
#                      in meters. For instance, 0.001 means 1mm
#                      of rain.
#   --temperature      Print data about temperature, as daily min,
#                      avg, and max temperatures. Values are in C.
#                      This is the default mode.
#   --runoff           Print data about daily overall runoff. This
#                      is in meters, 0.0001 means 1mm runoff.
#   --surfacerunoff    Print data about daily surface runoff. This
#                      is in meters, 0.0001 means 1mm runoff.
#   --subsurfacerunoff Print data about daily sub-surface runoff. This
#                      is in meters, 0.0001 means 1mm runoff.
#   --runoffrate       Print data about average daily surface runoff
#                      rate, i.e., kg / (m^2 s^1).
#   --evaporation      Print data about daily evaporation. This is in
#                      meters, 0.0001 means 1mm water equivalent
#                      evaporation.
#   --snowevaporation  Print data about daily evaporation of snow. This
#                      is in meters, 0.0001 means 1mm water equivalent
#                      evaporation.
#   --snowdepth        Print data about snow depth. The depth is
#                      represented by meters of water that the snow
#                      covering the area would melt as, if the snow
#                      were turned into water.
#   --plot             Plot the selected graph as graphics.
#   --debug            Turn on debugging printouts.
#

import sys
import cdsapi
import netCDF4
from netCDF4 import num2date
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import seaborn as sns
from datetime import datetime, timedelta
import pandas as pd
from tabulate import tabulate
import re

invalid1 = -1.0842e-19
invalid2 = -5.20417e-18
invalid3 = 2.64698e-23
invalid4 = 6.35275e-22
debug = 0

def fatalerr(x):
    print("Fatal error: " + x + " -- exit")
    SystemExit(1)

def printdebug(x):
    if (debug != 0):
        print(x)
        
def isoption(x):
    if (len(x) > 0 and x[0] == '-'):
        return(1)
    else:
        return(0)

def dfcols(df):
    return(len(df.columns))

def dfrows(df):
    return(len(df.index))

def dfreplacevalle(df,col,val,newval):
    count = 0
    for row in range(dfrows(df)):
        if (df.iloc[row,col] <= val):
            df.iloc[row,col] = newval
            count = count+1
    #print("replaced " + str(count) + " occurrences")

def dfreplacevaleq(df,col,val,newval):
    count = 0
    for row in range(dfrows(df)):
        if (df.iloc[row,col] == val):
            df.iloc[row,col] = newval
            count = count+1
    #print("replaced " + str(count) + " occurrences")

def cdgetcol(cd,col):
    printdebug("get column " + col)
    result = cd.variables[col][:].flatten()
    printdebug("got column " + col + ": length = " + str(len(result)) + " type = " + str(type(result)))
    result = result.compressed().tolist()
    printdebug("got list column " + col + ": length = " + str(len(result)) + " type = " + str(type(result)))
    return(result)

def read_netcdf_files(file_locations):
    t2m = []
    precip = []
    runoff = []
    surfacerunoff = []
    subsurfacerunoff = []
    runoffrate = []
    evaporation = []
    snowevaporation = []
    snowdepth = []
    time = []
    start_time = datetime.strptime("01/01/1900 00:00", "%d/%m/%Y %H:%M")
    date_points = []
    time_points = []

    for file_location in file_locations:
        f = netCDF4.Dataset(file_location) # open the .nc file
        printdebug("Opened file " + file_location)
        printdebug("t2m length now " + str(len(t2m)))
        printdebug("Variables: ")
        printdebug(f.variables)
        t2m += cdgetcol(f,'t2m')
        precip += cdgetcol(f,'cp')
        runoff += cdgetcol(f,'ro')
        surfacerunoff += cdgetcol(f,'sro')
        subsurfacerunoff += cdgetcol(f,'ssro')
        runoffrate += cdgetcol(f,'mror')
        evaporation += cdgetcol(f,'e')
        snowevaporation += cdgetcol(f,'es')
        snowdepth += cdgetcol(f,'sd')
        thistime = cdgetcol(f,'time')
        time += thistime
        for x in range(len(thistime)):
            #hours_from_start_time = start_time + timedelta(hours=int(time.data[x]))
            hours_from_start_time = start_time + timedelta(hours=int(thistime[x]))
            date_part = hours_from_start_time.strftime("%Y/%m/%d")
            time_part = hours_from_start_time.strftime("%H:%M:%S")
            date_points.append(date_part)
            time_points.append(time_part)
        printdebug("time len " + str(len(time)))
        printdebug("date_points len " + str(len(date_points)))
        printdebug("time_points len " + str(len(time_points)))
        printdebug("t2m len " + str(len(t2m)))
        printdebug("precip len " + str(len(precip)))
        printdebug("runoff len " + str(len(runoff)))
        printdebug("surfacerunoff len " + str(len(surfacerunoff)))
        printdebug("subsurfacerunoff len " + str(len(subsurfacerunoff)))
        printdebug("runoffrate len " + str(len(runoffrate)))
        printdebug("evaporation len " + str(len(evaporation)))
        printdebug("evaporation list " + str(evaporation))
        printdebug("snowevaporation len " + str(len(snowevaporation)))
        printdebug("snowdepth len " + str(len(snowdepth)))
        f.close()
        #printdebug(f)
    values = pd.DataFrame({
        # Convert temperatures from Kelvin to Celsius, i.e., subtract 273.15
        # "t2m"            : [x-273.15 for x in t2m.data if x!= -32767],
        "t2m"              : [x-273.15 for x in t2m if x!= -32767],
        "precip"           : precip,
        "runoff"           : runoff,
        "surfacerunoff"    : surfacerunoff,
        "subsurfacerunoff" : subsurfacerunoff,
        "runoffrate"       : runoffrate,
        "evap"             : evaporation,
        "snowevap"         : snowevaporation,
        "snowdepth"        : snowdepth,
        "date"             : date_points,
        "time"             : time_points
        })
    return(values)

def sumprecip(values):
    summed_values = values.groupby("date").sum("cp")
    final_values = summed_values.loc[:, ["precip"]]
    dfreplacevalle(final_values,0,invalid1,0.0)
    dfreplacevalle(final_values,0,invalid2,0.0)
    return(final_values)

def sumevap(values):
    summed_values = values.groupby("date").sum("e")
    final_values = summed_values.loc[:, ["evap"]]
    dfreplacevaleq(final_values,0,invalid1,0.0)
    dfreplacevaleq(final_values,0,invalid2,0.0)
    return(final_values)

def sumsnowevap(values):
    summed_values = values.groupby("date").sum("se")
    final_values = summed_values.loc[:, ["snowevap"]]
    dfreplacevaleq(final_values,0,invalid1,0.0)
    dfreplacevaleq(final_values,0,invalid2,0.0)
    return(final_values)

def avgtemp(values):
    daily_min_values = values.groupby("date").min("t2m")
    daily_avg_values = values.groupby("date").mean("t2m")
    daily_max_values = values.groupby("date").max("t2m")
    final_min_values = daily_min_values.loc[:, ["t2m"]]
    final_min_values.rename(columns={'t2m': 'min t2m'}, inplace=True)
    final_avg_values = daily_avg_values.loc[:, ["t2m"]]
    final_avg_values.rename(columns={'t2m': 'avg t2m'}, inplace=True)
    final_max_values = daily_max_values.loc[:, ["t2m"]]
    final_max_values.rename(columns={'t2m': 'max t2m'}, inplace=True)
    return(dfmergebydate3(final_min_values,final_avg_values,final_max_values))

def sumrunoff(values):
    summed_values = values.groupby("date").sum("runoff")
    final_values = summed_values.loc[:, ["runoff"]]
    dfreplacevalle(final_values,0,invalid1,0.0)
    dfreplacevalle(final_values,0,invalid2,0.0)
    return(final_values)

def sumsurfacerunoff(values):
    summed_values = values.groupby("date").sum("surfacerunoff")
    final_values = summed_values.loc[:, ["surfacerunoff"]]
    dfreplacevalle(final_values,0,invalid1,0.0)
    dfreplacevalle(final_values,0,invalid2,0.0)
    dfreplacevalle(final_values,0,invalid3,0.0)
    dfreplacevalle(final_values,0,invalid4,0.0)
    return(final_values)

def sumsubsurfacerunoff(values):
    summed_values = values.groupby("date").sum("subsurfacerunoff")
    final_values = summed_values.loc[:, ["subsurfacerunoff"]]
    dfreplacevalle(final_values,0,invalid1,0.0)
    dfreplacevalle(final_values,0,invalid2,0.0)
    dfreplacevalle(final_values,0,invalid3,0.0)
    dfreplacevalle(final_values,0,invalid4,0.0)
    return(final_values)

def avgrunoffrate(values):
    daily_values = values.groupby("date").mean("runoffrate")
    final_values = daily_values.loc[:, ["runoffrate"]]
    return(final_values)

def avgsnowdepth(values):
    daily_values = values.groupby("date").mean("snowdepth")
    final_values = daily_values.loc[:, ["snowdepth"]]
    return(final_values)

def combined(values):
    precip_values = sumprecip(values)
    evap_values = sumevap(values)
    snowevap_values = sumsnowevap(values)
    runoff_values = sumrunoff(values)
    surfacerunoff_values = sumsurfacerunoff(values)
    subsurfacerunoff_values = sumsubsurfacerunoff(values)
    snowdepth_values = avgsnowdepth(values)
    temp_values = avgtemp(values)
    return(dfmergebydate8(precip_values,
                          evap_values,
                          snowevap_values,
                          runoff_values,
                          surfacerunoff_values,
                          subsurfacerunoff_values,
                          temp_values,
                          snowdepth_values))

def dfmergebydate2(df1,df2):
    return(pd.merge(df1,df2,on="date"))

def dfmergebydate3(df1,df2,df3):
    return(dfmergebydate2(dfmergebydate2(df1,df2),
                          df3))

def dfmergebydate4(df1,df2,df3,df4):
    return(dfmergebydate2(dfmergebydate2(df1,df2),
                          dfmergebydate2(df3,df4)))

def dfmergebydate5(df1,df2,df3,df4,df5):
    return(dfmergebydate2(dfmergebydate4(df1,df2,df3,df4),
                          df5))

def dfmergebydate6(df1,df2,df3,df4,df5,df6):
    return(dfmergebydate2(dfmergebydate5(df1,df2,df3,df4,df5),
                          df6))

def dfmergebydate7(df1,df2,df3,df4,df5,df6,df7):
    return(dfmergebydate2(dfmergebydate6(df1,df2,df3,df4,df5,df6),
                          df7))

def dfmergebydate8(df1,df2,df3,df4,df5,df6,df7,df8):
    return(dfmergebydate2(dfmergebydate7(df1,df2,df3,df4,df5,df6,df7),
                          df8))

def nicetabulate(df,csv):
    #
    # Decide output format
    #
    if (csv):
        printdebug("doing csv")
        useformat = "tsv"
    else:
        printdebug("not doing csv")
        useformat = "simple"
    #
    # Do the tabulation
    #
    result = tabulate(df, headers = 'keys', tablefmt = useformat)
    #
    # Since some versions don't seem to support tsv format, if there's
    # space left in the input, replace them with commas.
    #
    if (csv):
        result = re.sub(r"[ 	]+",",",result)
    #
    # Done!
    #
    return(result)

def dfplot(df):
    #
    # Subfunction for configuring plot axis
    def configureaxes(ax):
        ax.tick_params(axis ='x', rotation = 90)
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1)))
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
        #ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        for label in ax.get_xticklabels(which='major'):
            label.set(rotation=30, horizontalalignment='right')
    #
    # dfplat continues here
    #
    fig = plt.figure(figsize=(17,6))
    plt.xlabel("Date");
    for col in df.columns:
        if (col == "min t2m" or col == "max t2m"):
            ax = sns.lineplot(data = df, x= 'date', y=col,
                              color='pink',
                              linewidth=0.5,
                              linestyle='--')
            configureaxes(ax)
        if (col == "avg t2m"):
            ax = sns.lineplot(data = df, x= 'date', y=col,
                              color='red')
            configureaxes(ax)
        if (col == "precip"):
            ax = sns.lineplot(data = df, x= 'date', y=col,
                              color='blue')
            configureaxes(ax)
        if (col == "snowdepth"):
            ax = sns.lineplot(data = df, x= 'date', y=col,
                              color='black')
            configureaxes(ax)
        if (col == "runoff"):
            ax = sns.lineplot(data = df, x= 'date', y=col,
                              color='green')
            configureaxes(ax)
        if (col == "surfacerunoff"):
            ax = sns.lineplot(data = df, x= 'date', y=col,
                              color='green')
            configureaxes(ax)
        if (col == "subsurfacerunoff"):
            ax = sns.lineplot(data = df, x= 'date', y=col,
                              color='green')
            configureaxes(ax)
        if (col == "evap"):
            ax = sns.lineplot(data = df, x= 'date', y=col,
                              color='yellow')
            configureaxes(ax)
        if (col == "evap"):
            ax = sns.lineplot(data = df, x= 'date', y=col,
                            color='grey')
            configureaxes(ax)
        if (col == "snowevap"):
            ax = sns.lineplot(data = df, x= 'date', y=col,
                              color='yellow')
            configureaxes(ax)
    plt.show()

def main():
    mode = "combined"
    plot = 0
    csv = 0
    file_names = ["data.nc"]
    file_names_given = 0
    #
    # Inner function 'processoption'
    #
    def processoption(opt,i,argv):
        nonlocal mode
        nonlocal csv
        nonlocal plot
        global debug
        if (opt == "--temperature"):
            mode = "temperature"
            return(0)
        elif (opt == "--full"):
            mode = "full"
            return(0)
        elif (opt == "--precipitation"):
            mode = "precipitation"
            return(0)
        elif (opt == "--runoff"):
            mode = "runoff"
            return(0)
        elif (opt == "--surfacerunoff"):
            mode = "surfacerunoff"
            return(0)
        elif (opt == "--subsurfacerunoff"):
            mode = "subsurfacerunoff"
            return(0)
        elif (opt == "--runoffrate"):
            mode = "runoffrate"
            return(0)
        elif (opt == "--evaporation"):
            mode = "evaporation"
            return(0)
        elif (opt == "--snowevaporation"):
            mode = "snowevaporation"
            return(0)
        elif (opt == "--snowdepth"):
            mode = "snowdepth"
            return(0)
        elif (opt == "--combined"):
            mode = "combined"
            return(0)
        elif (opt == "--text"):
            csv = 0
            return(0)
        elif (opt == "--csv"):
            csv = 1
            return(0)
        elif (opt == "--debug"):
            debug = 1
            return(0)
        elif (opt == "--plot"):
            plot = 1
            return(0)
        else:
            fatalerr("Unrecognised option " + opt)
            return(0)
    #
    # Inner function 'processargs'
    #
    def processargs():
        #print("Processing arguments...")
        #print(f"Arguments count: {len(sys.argv)}")
        nonlocal file_names
        file_name_set = 0
        skipn = 0
        for i, arg in enumerate(sys.argv):
            #print("Processing argument " + arg)
            if (i == 0):
                continue
            elif (skipn > 0):
                skipn = skipn - 1
                #print("Skipped an argument")
            else:
                if (isoption(arg)):
                    skipn = processoption(arg,i,sys.argv)
                else:
                    if (file_name_set == 0):
                        file_names = [arg]
                        file_name_set = 1
                    else:
                        file_names.append(arg)
    #
    # Back to the main function
    #
    processargs()
    #
    # Do the main function
    #
    weather_data = read_netcdf_files(file_names)
    if (mode == "full"):
        print(nicetabulate(weather_data, csv))
    else:
        if (mode == "precipitation"):
            processed_data = sumprecip(weather_data)
        elif (mode == "temperature"):
            processed_data = avgtemp(weather_data)
        elif (mode == "runoff"):
            processed_data = sumrunoff(weather_data)
        elif (mode == "surfacerunoff"):
            processed_data = sumsurfacerunoff(weather_data)
        elif (mode == "subsurfacerunoff"):
            processed_data = sumsubsurfacerunoff(weather_data)
        elif (mode == "runoffrate"):
            processed_data = avgrunoffrate(weather_data)
        elif (mode == "evaporation"):
            processed_data = sumevap(weather_data)
        elif (mode == "snowevaporation"):
            processed_data = sumsnowevap(weather_data)
        elif (mode == "snowdepth"):
            processed_data = avgsnowdepth(weather_data)
        elif (mode == "combined"):
            processed_data = combined(weather_data)
        else:
            fatalerr("Invalid mode " + mode)
        if (plot != 0):
            dfplot(processed_data)
        else:
            print(nicetabulate(processed_data, csv))

#
# Call the main program
#

main()
