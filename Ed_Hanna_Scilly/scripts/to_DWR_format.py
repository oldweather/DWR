#!/usr/bin/env python

# Convert the digitised data from Ed Hanna's files to the format
#  Ed Hawkins is using.

import os
import os.path
import pandas
import calendar
import sys

# Get script directory
sd=os.path.dirname(os.path.abspath(__file__))

# Location details - St Mary's Coast Guard station
# Information from Ed Hanna and Rob Allan
Station={'Name'     : 'SCILLY',
         'Latitude' : 49.9283,
         'Longitude': -6.3038,
         'Height1'  : 19.8, # barometer m asl up to April 1901
         'Height2'  : 43.3, # barometer m asl after April 1901
}
# Times are believed to be in UTC - no conversion necessary

ddir='../scilly_pressure_ditigised_1875to1901/as_csv'
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
