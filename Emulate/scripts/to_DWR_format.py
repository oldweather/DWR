#!/usr/bin/env python

# Convert the digitised data from Rob's Emulate files to the format
#  Ed Hawkins is using.

import os
import os.path
import pandas
import numpy
import datetime
import calendar
import sys

# Get script directory
sd=os.path.dirname(os.path.abspath(__file__))

# Load the Station names and locations
md=pandas.read_csv("%s/../../Lisa_storms/metadata/names.csv" % sd,
                   header=None)

# Get station name from file name
def get_station_name(file_name):
    sn=os.path.basename(file_name).split('.')
    if sn[0]=='DWR_stations':
        return sn[1].upper()
    return sn[0].upper()

# The old Emulate data is in several different formats.
# These files are in one-ob-per-day format
Files_opd=(
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
    'DWR_stations.Rochefort.csv',      # Changes to TPD in 1871
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
# These files are in two-ob-per-day format
Files_tpd=(
    'DWR_stations.Nairn.csv',
    'DWR_stations.Penzance.csv',
    'DWR_stations.Scarborough.csv',
    'DWR_stations.Greencastle.csv',    # Changes from OPD in 1868
    'DWR_stations.Rochefort.csv',      # Changes from OPD in 1871
)

def load_from_file_opd(file_name):
    station=get_station_name(file_name)
    csv=pandas.read_csv(file_name,header=None)

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
                dates.append(datetime.datetime(year,month,day,0)+
                             datetime.timedelta(hours=hour)))
                pressures.append(pre)
        return {'dates':dates,'pressures':pressures}

    year_i=find_year_starts(csv)
    file_data={}
    for idx in year_i:
         year=int(csv.iloc[idx,0])
         file_data["%04d" % year]=get_data_for_year(station,csv,idx)
    return file_data

def load_from_file_tpd(file_name):
    station=get_station_name(file_name)
    csv=pandas.read_csv(file_name,header=None)

    # Find the index numbers starting the data for a year
    #  (Lines with 'January' in the third column)
    def find_year_starts(tab):
        return tab[tab.iloc[:,2].str.contains('January',na=False)].index.values

    # Extract a year's worth of data given the start location
    def get_data_for_year(station,tab,istart):
        dates=[]
        pressures=[]
        year=int(tab.iloc[istart,0])
        for month in range(1,13):
            lastday=calendar.monthrange(year,month)[1]
            for day in range(1,lastday+1):
                for hri in (0,1):
                    if hri==0:
                        pre=tab.iloc[istart+day*2,month]
                    else:
                        pre=tab.iloc[istart+day*2+1,month]
                    try:
                        pre=float(pre)
                        if numpy.isnan(pre): continue
                        if pre<0: continue         # -9999 - missing
                        if pre<35: pre=pre*33.8639 # InHg
                        if pre<800: pre=pre*1.33   # mmHg
                    except ValueError:
                        continue
                    if hri==0:
                        dates.append(datetime.datetime(year,month,day,8))
                    else:
                        dates.append(datetime.datetime(year,month,day,8))
                    pressures.append(pre)
        return {'dates':dates,'pressures':pressures}
    

# Add a station's data to the output files
def output_station(name,sdata):
    LastF=''
    Of=None
    mdl=md[md.iloc[:,0].str.lower()==name.lower()]
    if mdl.empty:
        raise StandardError("No station %s in metadata" % 
                                            std.iloc[ln,0])
    for idx in range(len(sdata['dates'])):
        Of=("%s/../../data_from_Emulate/%04d/%02d/prmsl.txt" %
                         (sd,sdata['dates'][idx].year,
                             sdata['dates'][idx].month))
        if Of!=LastF:
            dn=os.path.dirname(Of)
            if not os.path.isdir(dn):
                os.makedirs(dn)
            if opfile is not None:
                opfile.close()
                if os.path.getsize(LastF)==0:
                    os.remove(Of)
                    dn=os.path.dirname(LastF)
                    if not os.listdir(dn):
                        os.rmdir(dn)
            opfile=open(Of, "a")
            LastF=Of

            opfile.write(("%04d %02d %02d %02d %02d %6.2f "+
                          "%7.2f %6.1f %16s\n") %
                         (sdata['dates'][idx].year,
                          sdata['dates'][idx].month,
                          sdata['dates'][idx].day,
                          sdata['dates'][idx].hour,
                          sdata['dates'][idx].minute,
                          mdl.iloc[0,2],mdl.iloc[0,3], #latlon
                          sdata['pressures'][idx],     # ob value
                          mdl.iloc[0,1]))              # name
     

# Load all the data
emulate_data={}
for file_name in Files:
    station_name=get_station_name(file_name)
    print station_name

    # Once-per-day data
    if file_name in Files_opd:
        emulate_data[station_name].update(load_from_file_opd(
                     "%s/../original_data_csv/%s" % (sd,file_name)))
    
    # Twice_per_day data
    if file_name in Files_opd:
        emulate_data[station_name].update(load_from_file_tpd(
                     "%s/../original_data_csv/%s" % (sd,file_name)))
    
    # Special cases
    emulate_data['Teneriffe']=load_from_file_teneriffe(
                     "%s/../original_data_csv/Teneriffe.Teneriffe.csv" % sd)
