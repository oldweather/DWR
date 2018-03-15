#!/usr/bin/env python

# Convert the digitised data from Lisa's files to the format Ed is
#  using.

import os
import os.path
import pandas
import glob
import datetime
import sys

# Get script directory
sd=os.path.dirname(os.path.abspath(__file__))

# Load the Station names and locations
md=pandas.read_csv("%s/../metadata/names.csv" % sd,
                   header=None)


# The data in Lisa's files is stored as 8 values/day, but the mapping of
#  the values onto GMT times is peculiar and time varying. Return the
#  time offset (hours) for the given date and value, from the date given
#  in the file (assuming times are 0,3,..,21)
def get_time_offset(date,hours):
   # Before April 1922 - at 1,7,13,18 and back by 1/2 day
    offsets=(-14,-14,-15,-15,-14,-14,-14,-14)
   # At beginning of April 1921, move forward by 1 day
    if date.year>1944 or (date.year==1944 and date.month>7):
        offsets=(10,10,9,9,10,10,10,10)
    # At beginning of August 1944, switched to 0,6,12,18
    if date.year>1944 or (date.year==1944 and date.month>7):
        offsets=(9,9,9,9,9,9,9,9)
    return offsets[hours/3]
   
# Convert Lisa's data
Lf=glob.glob("%s/../raw.data/*.dat" % sd)
for stfile in Lf:
    std=pandas.read_fwf(stfile,
                        widths=(24,5,3,3,7,7,7,7,7,7,7,7),
                        header=None)
    # Append each line to the new ouput file
    #  slow - but so what.
    for ln in range(0,len(std.iloc[:,0])):
        Of=("%s/../../data_from_Lisa/%04d/%02d/prmsl.txt" %
                          (sd,std.iloc[ln,1],std.iloc[ln,2]))
        mdl=md[md.iloc[:,0].str.lower()==std.iloc[ln,0].lower()]
        if mdl.empty:
            raise StandardError("No station %s in metadata" % 
                                                std.iloc[ln,0])
        LastF=''
        Of=None
        opfile=None
        ob_tbase=datetime.datetime(std.iloc[ln,1],
                                   std.iloc[ln,2],
                                   std.iloc[ln,3],0)
        for hri in range(1,9):
            # Skip the missing data
            if std.iloc[ln,hri+3]>9000: continue
            # Ob time and date
            ob_time=ob_tbase+datetime.timedelta(hours=
               (hri-1)*3 + get_time_offset(ob_tbase,(hri-1)*3))
            # Output value in Ed's format
            Of=("%s/../../data_from_Lisa/%04d/%02d/prmsl.txt" %
                             (sd,ob_time.year,ob_time.month))
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
                         (ob_time.year,ob_time.month,
                          ob_time.day,ob_time.hour,
                          ob_time.minute,
                          mdl.iloc[0,2],mdl.iloc[0,3], #latlon
                          std.iloc[ln,hri+3],          # ob value
                          mdl.iloc[0,1]))              # name
