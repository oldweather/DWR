#!/usr/bin/env python

# Convert the digitised data from Rob's Emulate files to the format
#  Ed Hawkins is using.

# The old Emulate data is in several different formats. This script does
# The block-table one-ob-per-day style.

Hours={
    'Lyons':      9,
    'Alexandria': 9,
    'Sibu':       8,
    'Stornoway':  9,
    'Brest':      8, # Change to 18 previous day on 1875-04-01
    'Rochefort':  8,
    'Mogador':    7,
    'Biskra':     7,
}    

Height={
    'Rome':       50,
    'Stornoway':  21,
    'Biskra':    124.6,
    'Angra':      54,
    'Funchal':    25,
}    
        
Files=(
    'Alexandria.Alexandria.csv',
    'DWR_stations.Aberdeen.csv',
    'DWR_stations.Algiers.csv',
    'DWR_stations.Angra.csv',
    'DWR_stations.Biskra.csv',
    'DWR_stations.Brest.csv',
    'DWR_stations.Funchal.csv',
    'DWR_stations.Galway.csv',
    'DWR_stations.Greencastle.csv',    # Changes to TPD in 1868
    'DWR_stations.Holyhead.csv',
    'DWR_stations.La Coruna.csv',
    'DWR_stations.Liverpool.csv',
    'DWR_stations.Mogador.csv',
    'DWR_stations.Pembroke.csv',
    'DWR_stations.Plymouth.csv',
    'DWR_stations.Portsmouth.csv',
    'DWR_stations.Rochefort.csv'   ,   # Changes to TPD in 1871
    'DWR_stations.Roches Pt.csv',
    'DWR_stations.Scilly Islands.csv',
    'DWR_stations.Toulon.csv',
    'DWR_stations.Valentia.csv',
    'Lesina_Split.Sheet1.csv',
    'Lisbon.Lisbon.csv',
    'Lyons.Lyons.csv',
    'Rome.Rome.csv',
    'Sibiu.Funchal.csv',
    'Stornaway.Stornaway.csv',
)


import os
import os.path
import pandas
import numpy
import datetime
import calendar
import sys

# Get script directory
sd=os.path.dirname(os.path.abspath(__file__))

# Functions to get data out of the tabular Excel format

# Hour (gmt) of the daily ob.
def obs_hour(station,year,month):
    if station=='Brest':
        if year>1875 or (year==1875 and month>3):
            return -6
    return Hours.get(station,8)

# Find the index numbers starting the data for a year
#  (Lines with 'January' in the second column)
def find_year_starts(tab):
    return tab[tab.iloc[:,1].str.contains('January',na=False)].index.values

# Extract a year's worth of data given the start location
def get_data_for_year(station,tab,istart):
    dates=[]
    pressures=[]
    year=int(tab.iloc[istart,0])
    for month in range(1,13):
        hour=obs_hour(station,year,month)
        lastday=calendar.monthrange(year,month)[1]
        for day in range(1,lastday+1):
            pre=tab.iloc[istart+day+1,month]
            try:
                pre=float(pre)
                if numpy.isnan(pre): continue
                if pre<0: continue         # -9999 - missing
                if pre<35: pre=pre*33.8639 # InHg
                if pre<800: pre=pre*1.33   # mmHg
            except ValueError:
                continue
            dates.append(datetime.datetime(year,month,day,hour))
            pressures.append(pre)
    return {'dates':dates,'pressures':pressures}

# Get station name from file name
def get_station_name(file_name):
    sn=os.path.basename(file_name).split('.')
    if sn[0]=='DWR_stations':
        return sn[1].upper()
    return sn[0].upper()

# Load all station data from a file name
def load_from_file(file_name):
    station=get_station_name(file_name)
    csv=pandas.read_csv(file_name,header=None)
    year_i=find_year_starts(csv)
    file_data={}
    for idx in year_i:
         year=int(csv.iloc[idx,0])
         file_data["%04d" % year]=get_data_for_year(station,csv,idx)
    return file_data

# Load all the data
emulate_data={}
for file_name in Files:
    station_name=get_station_name(file_name)
    print station_name
    emulate_data[station_name]=load_from_file(
                 "%s//../original_data_csv/%s" % (sd,file_name))

