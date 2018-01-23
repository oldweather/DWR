# (C) British Crown Copyright 2017, Met Office
#
# This code is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
"""
The functions in this module provide the main way to load
DWR observations.
"""

import os
import os.path
import datetime
import pandas

def get_data_dir():
    scratch=os.getenv('SCRATCH')
    if scratch is None:
        raise StandardError("SCRATCH environment variable is undefined")
    base_file = "%s/DWR" % scratch
    if os.path.isdir(base_file):
        return base_file
    raise StandardError("Scratch directory %s does not exist" % scratch)

def get_data_file_name(variable,year,month):
    """Return the name of the file containing data for the
       requested variable, at the specified time."""
    base_dir=get_data_dir()
    name="%s/%04d/%02d/%s.txt" % (base_dir,
                                  year,month,variable)
    return name

def get_obs_1file(variable,year,month):
    """Retrieve all the observations in a single file."""
    of_name=get_data_file_name(variable,year,month)
    if not os.path.isfile(of_name):
        raise IOError("No obs file for %s on %04d/%02d" % (variable,year,month))

    o=pandas.read_table(of_name,sep='\s+',
                       header=None,
                       encoding="ascii",
                       names=['year','month','day','hour','minute',
                              'latitude','longitude',
                              'value',
                              'name'],
                       converters={'year': int, 'month': int, 'day' : int,
                                   'hour': int, 'minute': int,
                                   'latitude': float,'longitude': float,
                                   'value': float,
                                   'name': str},
                       na_values=['NA'],
                       comment=None)
    # Add the datetime
    o=o.assign(dtm=pandas.to_datetime(o[['year','month','day','hour','minute']]))
    return o
 
def get_obs(start,end,variable):
    """Retrieve all the observations between start and end"""
    result=None
    ct=start
    while(ct<end):
        o=get_obs_1file(variable,ct.year,ct.month)
        o2=o[(o.dtm>=start) & (o.dtm<end)]
        if(result is None):
            result=o2
        else:
            result=pandas.concat([result,o2])
        ct=add_one_month(ct)
    return result

# Want to move a datetime to the next month
#  don't care about preserving the day of month
def add_one_month(dt0):
    dt1 = dt0.replace(day=1)
    dt2 = dt1 + datetime.timedelta(days=32)
    dt3 = dt2.replace(day=1)
    return dt3

# Get the observation at the station interpolated to the desired time
def at_station_and_time(obs,station,dte):
    at_station=obs.loc[obs['name']==station]
    if at_station.empty:
        raise StandardError('No data for station %s' % station)
    at_station=at_station.sort_values(by='dtm',ascending=True)
    hit=at_station.loc[at_station['dtm']==dte]
    if not hit.empty:
        return hit['value'].values[0]
    before=at_station.loc[at_station['dtm']<dte]
    if before.empty:
        raise StandardError('No data for station %s before %s' % (station,
                     dte.strftime("%Y-%m-%d:%H:%M")))
    before=before.iloc[-1] # last row
    after=at_station.loc[at_station['dtm']>dte]
    if after.empty:
        raise StandardError('No data for station %s after %s' % (station,
                     dte.strftime("%Y-%m-%d:%H:%M")))
    after=after.iloc[0] # first row
    weight=((dte-before['dtm']).total_seconds()/
           (after['dtm']-before['dtm']).total_seconds())
    return after['value']*weight+before['value']*(1-weight)

# Get the position of a named station
def get_station_location(obs,station):
    at_station=obs.loc[obs['name']==station]
    if at_station.empty:
        raise StandardError('No data for station %s' % station)
    result={'latitude': at_station['latitude'].values[0],
            'longitude':at_station['longitude'].values[0]}
    return result
