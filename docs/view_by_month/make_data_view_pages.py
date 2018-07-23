#!/usr/bin/env python

# Make a documentation page for each data file

import os

# Make the index page
with open("months.rst",'w') as ofile:
    ofile.write("Data month-by-month\n")
    ofile.write("===================\n\n")
    ofile.write(".. include:: file_header.rst\n\n")
    ofile.write(".. list-table:: \n")
    ofile.write("   :widths: 15 10 10 10 10 10 10 10 10 10 10 10 10\n")
    ofile.write("   :header-rows: 1\n\n")
    ofile.write("   * - Year \n") 
    ofile.write("     - Jan \n")
    ofile.write("     - Feb\n")
    ofile.write("     - Mar\n")
    ofile.write("     - Apr\n")
    ofile.write("     - May\n")
    ofile.write("     - Jun\n")
    ofile.write("     - Jul\n")
    ofile.write("     - Aug\n")
    ofile.write("     - Sep\n")
    ofile.write("     - Oct\n")
    ofile.write("     - Nov\n")
    ofile.write("     - Dec\n")
    for year in range(1856,1961):
        ofile.write("   * - %04d \n" % year) 
        for month in range(1,13):
            ofile.write("     - ")
            for var in (['prmsl']):
                dfile="../../data/%04d/%02d/%s.txt" % (year,month,var)
                if os.path.isfile(dfile):
                    ofile.write("`prmsl <https://github.com/oldweather/DWR/blob/master/"+
                                "data/%04d/%02d/%s.txt>`_\n" % (year,month,var))
                else:
                    ofile.write("\n")

