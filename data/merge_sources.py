#!/usr/bin/env python

# Merge the data from the different sources into a single file.

import os
import os.path

# Get script directory
sd=os.path.dirname(os.path.abspath(__file__))

sources=("%s/../data_from_Ed" % sd,
         "%s/../data_from_Ed_Hanna" % sd,
         "%s/../data_from_Lisa" % sd,
         "%s/../data_from_Emulate" % sd)

for year in range(1856,1961):
    for month in range (1,13):
        target_file="%s/%04d/%02d/prmsl.txt" % (sd,year,month)
        if os.path.isfile(target_file):
            os.remove(target_file)
        for source in sources:
            source_file="%s/%04d/%02d/prmsl.txt" % (source,year,month)
            if os.path.isfile(source_file):
                if not os.path.isdir(os.path.dirname(target_file)):
                    os.makedirs(os.path.dirname(target_file))
                with open(target_file, 'a') as outfile:
                    with open(source_file) as infile:
                        outfile.write(infile.read())
