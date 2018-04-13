#!/usr/bin/env python

# Convert the digitised data from Rob's Emulate files to the format
#  Ed Hawkins is using.

import os
import os.path
import pandas
import calendar
import sys

# Get script directory
sd=os.path.dirname(os.path.abspath(__file__))

# Functions to get data out of the tabular excel format

# Hour (gmt) of the daily ob.
def obs_hour(year,month):
    return 7

# Find the index numbers starting the data for a year
#  (Lines with 'January' in the second column)
def find_year_starts(tab):
    return tab[tab.iloc[:,1].str.contains('January',na=False)].index.values

# Extract a year's worth of data given the start location
def get_data_for_year(tab,istart):
    dates=[]
    pressures=[]
    year=int(tab.iloc[istart,0])
    for month in range(1,13):
        hour=obs_hour(year,month)
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
    csv=pandas.read_csv(file_name)
    year_i=find_year_starts(csv)
    file_data={}
    for idx in year_i:
         year=int(csv.iloc[idx,0])
         file_data["%04d" % year]=get_data_for_year(csv,idx)
    return file_data

# Load all the data
emulate_data={}
dfiles=os.listdir("%s/../original_data_csv" % sd)
for file_name in dfiles:
    station_name=get_station_name(file_name)
    emulate_data[station_name]=load_from_file(
                 "%s//../original_data_csv/%s" % (sd,file_name))




ddir='../original_data_csv'
for dfile in os.listdir(ddir):
    year=int(dfile[33:37])
    month_a=dfile[30:33].title() # 'Jan, 'Feb, 
    month=list(calendar.month_abbr).index(month_a) # 1, 2, 
    # Output value in Ed. Hawkins's format
    Of=("%s/../../data_from_Ed_Hanna/%04d/%02d/prmsl.txt" %
                     (sd,year,month))
    if not os.path.isdir(os.path.dirname(Of)):
        os.makedirs(os.path.dirname(Of))
    cs=pandas.read_csv("%s/%s" % (ddir,dfile),
                       na_values=('',"   ",'NODATA',
                                  'LOST?'))
    hours=[int(h)/100.0 for h in list(cs)[1:4]]
    with open(Of, 'w') as opfile:
        for index, row in cs.iterrows():
            if row.isnull()[0]: continue
            day=row[0]
            if isinstance(day,str):
                if len(day)>2: day=day[-2:]
            for hr in range(len(hours)):
                if row.isnull()[hr+1]: continue
                opfile.write(("%04d %02d %02d %02d %02d %6.2f "+
                              "%7.2f %6.1f %16s\n") %
                             (year,month,
                              int(day),              
                              int(hours[hr]),
                              int((hours[hr]%1)*60),    # minute
                              Station['Latitude'],
                              Station['Longitude'],
                              float(row[hr+1])*33.8639, # ob value (hPa)
                              Station['Name']))
