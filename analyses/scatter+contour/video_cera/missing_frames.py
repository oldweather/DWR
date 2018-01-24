#!/usr/bin/env python

# Find missing movie frames

import os
import subprocess
import datetime


start_day=datetime.datetime(1903, 10, 2, 0)
end_day  =datetime.datetime(1903, 10, 31, 15)

# Function to check if the job is already done for this timepoint
def is_done(year,month,day,hour):
    op_file_name="%s/images/DWR/scatter+contour.cera/Scatter+contour_%04d%02d%02d%02d%02d.png" % (
                 os.getenv('SCRATCH'),year,month,day,int(hour),int(hour%1*60))
    if os.path.isfile(op_file_name):
        return True
    return False

current_day=start_day
while current_day<=end_day:
       for fraction in (0,.25,.5,.75):
            if is_done(current_day.year,current_day.month,
                           current_day.day,current_day.hour+fraction):
                continue
            print "%04d-%02d-%02d:%02d:%02d" %(current_day.year,current_day.month,
                                                 current_day.day,current_day.hour,
                                                 int(fraction*60))
       current_day=current_day+datetime.timedelta(hours=1)
