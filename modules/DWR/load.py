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
        return base.file
    raise StandardError("Scratch directory %s does not exist")

def get_data_file_name(variable,year,month):
    """Return the name of the file containing data for the
       requested variable, at the specified time."""
    base_dir=get_data_dir()
    name="%s/%04d/%s/%02d.txt" % (base_dir,
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
                       names=['year','month','day','hour','Latitude','Longitude','value'],
                       converters={'year': int, 'month': int, 'day' : int,
                                   'hour': float,'Latitude': float,'Longitude': float,
                                   'Value': float},
                       na_values=['NA'],
                       comment=None)
    # Separate the hour and minute
    o.assign('minute',o.hour%100)
    o.hour=int(o.hour/100)
    # Add the datetime
    o.assign('datetime',pandas.to_datetime(o[['year','month','day','hour','minute']]))
    return o
 
def get_obs(start,end,variable):
    """Retrieve all the observations between start and end"""
    result=None
    ct=start
    while(ct<end):
        o=get_obs_1file(variable,ct.year,ct.month)
        o2=o[(datetime>=start) & (dtm<end)]
        if(result is None):
            result=o2
        else:
            result=pandas.concat([result,o2])
        ct=ct+datetime.timedelta(months=1)
    return result
