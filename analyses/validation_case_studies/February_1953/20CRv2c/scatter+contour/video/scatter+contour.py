#!/bin/env python

# UK region weather plot 
# 20CR2c pressures and validation against DWR

import os
import os.path
import math
import datetime
import collections

import matplotlib
from matplotlib.backends.backend_agg import \
                 FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import Meteorographica.data.twcr as twcr

import DWR

import local_plots
 
# Get the datetime to plot from commandline arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--year", help="Year",
                    type=int,required=True)
parser.add_argument("--month", help="Integer month",
                    type=int,required=True)
parser.add_argument("--day", help="Day of month",
                    type=int,required=True)
parser.add_argument("--hour", help="Time of day (0 to 23.99)",
                    type=float,required=True)
parser.add_argument("--opdir", help="Directory for output files",
           default=("%s/images/DWR/vcs_20CR2c_1953_scatter+contour" % 
                                             os.getenv('SCRATCH')),
                    type=str,required=False)
args = parser.parse_args()
if not os.path.isdir(args.opdir):
    os.makedirs(args.opdir)
 
dte=datetime.datetime(args.year,args.month,args.day,
                      int(args.hour),int(args.hour%1*60))

# HD video size 1920x1080
aspect=16.0/9.0
fig=Figure(figsize=(10.8*aspect,10.8),  # Width, Height (inches)
           dpi=100,
           facecolor=(0.88,0.88,0.88,1),
           edgecolor=None,
           linewidth=0.0,
           frameon=False,
           subplotpars=None,
           tight_layout=None)
canvas=FigureCanvas(fig)
font = {'family' : 'sans-serif',
        'sans-serif' : 'Arial',
        'weight' : 'normal',
        'size'   : 14}
matplotlib.rc('font', **font)

# Get all the DWR stations that appear in the month
obs=DWR.load_observations('prmsl',
                          datetime.datetime(1953,2,1,0),
                          datetime.datetime(1953,2,28,23))
# Remove stations already in ISPD
obs=obs[~obs['name'].isin(['LERWICK','STORNOWAY','VALENTIA',
                           'CULDROSE','GORLESTON','LEUCHARS'])]
obs=obs.sort_values(by='latitude',ascending=True)
stations=collections.OrderedDict.fromkeys(
                        obs.loc[:,'name']).keys()
latlon={}
for station in stations:
   latlon[station]=DWR.get_station_location(obs,station)

# Get the DWR observations within +- 15 hours
obs=DWR.load_observations('prmsl',
                          dte-datetime.timedelta(hours=15),
                          dte+datetime.timedelta(hours=15))
# Remove stations already in ISPD
obs=obs[~obs['name'].isin(['LERWICK','STORNOWAY','VALENTIA',
                           'CULDROSE','GORLESTON','LEUCHARS'])]
# sort them from north to south
obs=obs.sort_values(by='latitude',ascending=True)

# Get the reanalysis pressures and observations
prmsl=twcr.load('prmsl',args.year,args.month,args.day,
                             args.hour,version='2c')
prmsl.data=prmsl.data/100  #] convert to hPa
obs_t=twcr.load_observations_fortime(dte,version='2c')
# Filter to those near the UK # For speed only, optional
obs_t=obs_t.loc[((obs_t['Latitude']>0) & 
                   (obs_t['Latitude']<90)) &
                ((obs_t['Longitude']>240) | 
                   (obs_t['Longitude']<100))].copy()

local_plots.plot_scatter_contour(fig,prmsl,obs_t,obs,dte,
                                 stations=stations,
                                 station_latlon=latlon,
                                 label_mean_contour=False)

# Output as png
fig.savefig('%s/Scatter+contour_%04d%02d%02d%02d%02d.png' % 
                                      (args.opdir,args.year,
                                       args.month,args.day,
                                      int(args.hour),
                                      int(args.hour%1*60)))
