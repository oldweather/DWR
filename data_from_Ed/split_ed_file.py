#!/usr/bin/env python

# Split the data in the one big file Ed sent into monthly files.
# Note that Ed Hawkins's file also contains Ed Hanna's data.

import os
import os.path
import sys

# Get script directory
sd=os.path.dirname(os.path.abspath(__file__))

# Source file
infile="%s/DWR/dwr_mslp_forPhilip.txt" % os.getenv('SCRATCH')

# Copy into new target files line by line
with open(infile, 'r') as ifile:
    open_out=None
    line=ifile.readline()
    while line:
        year=int(line[0:4])
        month=int(line[5:7])
        target_file="%s/%04d/%02d/prmsl.txt" % (sd,year,month)
        if target_file != open_out:
            if open_out is not None:
                outfile.close()
            if not os.path.isdir(os.path.dirname(target_file)):
                 os.makedirs(os.path.dirname(target_file))
            outfile=open(target_file, 'a')
            open_out=target_file
        outfile.write(line)
        line=ifile.readline()
