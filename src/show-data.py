#
# Call as follows
#
#   python3 show-data.py [options] [file.nc]
#
# The command reads data pulled earlier by pull-data.py into file file.nc.
# It then proceeds to print the data in a convenient format. Options
# are used to control what is printed, e.g., precipation, temperature, etc.
#
# If no arguments are given, the file is assumed to be data.nc. If no
# options are given, the software behaves as if --temperature option was
# specified, i.e., daily temperatures from the data are shown.
#
# The possible options are:
#
#   --full             Print everything (for debugging etc)
#   --precipitation    Print data about precipitation, tabulated
#                      as daily preciptation -- rain or snow --
#                      in meters. For instance, 0.001 means 1mm
#                      of rain.
#   --temperature      Print data about temperature, as daily min,
#                      avg, and max temperatures. Values are in C.
#                      This is the default mode.
#   --runoff           Print data about average daily surface runoff.
#                      This is a rate, i.e., kg / (m^2 s^1).
#

import sys
import cdsapi
import netCDF4
from netCDF4 import num2date
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import pandas as pd
from tabulate import tabulate

def fatalerr(x):
    print("Fatal error: " + x + " -- exit")
    SystemExit(1)
    
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
    print("replaced " + str(count) + " occurrences")
    
def read_netcdf_file(file_location):
    f = netCDF4.Dataset(file_location) # This the python package I used to open the nc file
    #print("Variables: ")
    #print(f.variables)
    t2m = f.variables['t2m'][:].flatten()
    precip = f.variables['cp'][:].flatten()
    time = f.variables['time'][:].flatten()
    start_time = datetime.strptime("01/01/1900 00:00", "%d/%m/%Y %H:%M")
    date_points = []
    time_points = []
    for x in range(len(time)):
        hours_from_start_time = start_time + timedelta(hours=int(time.data[x]))
        date_part = hours_from_start_time.strftime("%Y/%m/%d")
        time_part = hours_from_start_time.strftime("%H:%M:%S")
        #split_time = hours_from_start_time.split();
        #date_part = split_time[0]
        #time_part = split_time[1]
        date_points.append(date_part)
        time_points.append(time_part)

    values = pd.DataFrame({
        "t2m"    : [x-273.15 for x in t2m.data if x!= -32767], # As we said the values are in Kelvin, to convert in Celsius we have to subtract 273.15
        "precip" : precip,
        "date"   : date_points,
        "time"   : time_points
        })
    return(values)

def sumprecip(values):
    summed_values = values.groupby("date").sum("cp")
    final_values = summed_values.loc[:, ["precip"]]
    dfreplacevalle(final_values,0,-5.20417e-18,0.0)
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
    return(pd.merge(pd.merge(final_min_values,final_avg_values,on="date"),final_max_values,on="date"))

def main():
    mode = "temperature"
    file_name = "data.nc"
    #
    # Inner function 'processoption'
    #
    def processoption(opt,i,argv):
        nonlocal mode
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
        else:
            fatalerr("Unrecognised option " + opt)
            return(0)
    #
    # Inner function 'processargs'
    #
    def processargs():
        print("Processing arguments...")
        #print(f"Arguments count: {len(sys.argv)}")
        nonlocal file_name
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
                        file_name = arg
                    else:
                        fatalerr("File name was already specified; too many arguments")
    #
    # Back to the main function
    #
    processargs()
    #
    # Do the main function
    #
    weather_data = read_netcdf_file(file_name)
    if (mode == "full"):
        print(tabulate(weather_data, headers = 'keys'))
    elif (mode == "precipitation"):
        processed_data = sumprecip(weather_data)
        print(tabulate(processed_data, headers = 'keys'))
    elif (mode == "temperature"):
        processed_data = avgtemp(weather_data)
        print(tabulate(processed_data, headers = 'keys'))
    elif (mode == "runoff"):
        processed_data = avgrunoff(weather_data)
        print(tabulate(processed_data, headers = 'keys'))
    else:
        fatalerr("Invalid mode " + mode)

#
# Call the main program
#

main()
