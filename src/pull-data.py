#
# Call as follows
#
#   python3 pull-data.py [options] [ystart [yend]]
#
# This pulls cave-relevant weather data from CDS. The argyument ystart
# should be a four-digit year number to start the pulling from, and
# the optional yend argument should another year to end the pulling
# from. If yend is not provided, just the starting year is pulled. If
# neither year value is provided, by default the command pulls just
# the year 2019.
#
# The command writes its output to a file data-ystart-yend.nc. You may
# later use the show-data.py program to print out the pulled data.
#
# The pull-data.py command may also invoked with options:
#
#   --month nn             Pull only month nn (expressed as a two-digit
#                          month number)
#
#   --months nn mm         Pull month nn to mm (expressed as a two-digit
#                          month numbers)
#
#   --coordinates lat lon  Use the coordinates 'lat' and 'lon'. By 
#                          default the command uses the corodinates of
#                          Njiellalanjävri in northern Finland.
#

import sys
import cdsapi
import netCDF4
from netCDF4 import num2date
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def fatalerr(x):
    print("Fatal error: " + x + " -- exit")
    SystemExit(1)
    
def isoption(x):
    if (len(x) > 0 and x[0] == '-'):
        return(1)
    else:
        return(0)

#    Input:
#        year, month, day, area, time, file_location: Strings
#    Outputs:
#        file_location: A string as in input

def getdata(year, month, day, area, time, file_location):
    c = cdsapi.Client() 
    c.retrieve(
        'reanalysis-era5-single-levels',{
            'product_type':'reanalysis', # This is the dataset produced by the CDS
            'variable':['2m_temperature','convective_precipitation','runoff','mean_runoff_rate','evaporation'],
            'year': year,
            'month': month,
            'day': day,
            'area': area,
            'time': time,
            'format':'netcdf' # The format we choose to use
        },
        file_location)
    return(file_location)

def main():
    latitude  = "69.232023" # Njiellalanjävri
    longitude = "21.420556"
    ystart = 2019 # latest year in the database
    yend = ystart
    months = ["01","02","03","04","05","06","07","08","09","10","11","12"] # all months
    #
    # Inner function 'constructyeartable'
    #
    def constructyeartable(ystart,yend):
        tab = []
        for year in range(ystart,yend+1):
            tab.append(str(year))
        return(tab)
    #
    # Inner function 'processoption'
    #
    def processoption(opt,i,argv):
        nonlocal months
        nonlocal latitude; 
        nonlocal longitude;
        if (opt == "--month"):
            if (i + 1 >= len(argv)):
                fatalerr("Expected an argument to follow --month option")
            month = argv[i+1]
            months = [month]
            return(1)
        elif (opt == "--months"):
            if (i + 2 >= len(argv)):
                fatalerr("Expected an argument to follow --month option")
            monthfrom = num(argv[i+1])
            monthto = num(argv[i+2])
            months = []
            for month in range(monthfrom,monthto+1):
                if (month < 10):
                    thismonth = "0" + str(month)
                else:
                    thismonth = str(month)
                months.append(thismonth)
            return(2)
        elif (opt == "--coordinates"):
            if (i + 2 >= len(argv)):
                fatalerr("Expected an argument to follow --coordinates option")
            latitude = num(argv[i+1])
            longitude= num(argv[i+2])
            return(2)
        else:
            fatalerr("Unrecognised option " + opt)
            return(0)
    #
    # Inner function 'processargs'
    #
    def processargs():
        print("Processing arguments...")
        #print(f"Arguments count: {len(sys.argv)}")
        nonlocal ystart;
        nonlocal yend;
        yearargs = 0
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
                    if (yearargs == 0):
                        ystart = int(arg)
                        yend = ystart
                        yearargs = 1
                    elif (yearargs == 1):
                        yend = int(arg)
                        yearargs = 2
                    else:
                        fatalerr("Too many arguments")
        #print("processed arguments...")
    #
    # Back to the main function
    #
    processargs()
    #
    # Set up the parameters
    #
    years = constructyeartable(ystart,yend)
    file_name = 'data-' + str(ystart) + "-" + str(yend) + ".nc"
    #
    # Now actually getting the data
    #
    print("Getting data from " + str(ystart) + " to " + str(yend) + " now...")
    print("Years = " + str(years))
    print("Months = " + str(months))
    print("File_name = " + file_name)
    file_location = getdata(
        year  = years,
    
        # NB: Single digits days or months must have 0s in front or that will cause an error
        day   = ['01', '02', '03','04', '05', '06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'],
        month = months,
    
        # The ERA5 accept rectangular shape grid as a searching areas
        # but we can use also input a point with this system:ß
        area  = latitude +'/'+ longitude +'/'+ latitude +'/'+ longitude,

        # Get all hours to get the precipation data right
        time = ['00:00','01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00',],
        # We can request one per each day
        # time  = ['14:00'], # noon in Finland
        file_location = file_name)
    #
    # Done!
    #
    print("Done")

main()
