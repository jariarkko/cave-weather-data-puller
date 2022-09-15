import cdsapi
import netCDF4
from netCDF4 import num2date
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import pandas as pd
from tabulate import tabulate

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
    print("final_values rows " + str(dfrows(final_values)))
    print("final_values cols " + str(dfcols(final_values)))
    dfreplacevalle(final_values,0,-5.20417e-18,0.0)
    return(final_values)

weather_data = read_netcdf_file('data.nc')

# print(weather_data)

summode = 1

if summode != 0:
    summed_data = sumprecip(weather_data)
    print(tabulate(summed_data, headers = 'keys'))
else:
    print(tabulate(weather_data, headers = 'keys'))
