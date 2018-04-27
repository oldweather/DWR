#!/bin/env python

## UK region weather plot 
# 20CR3 pressures and validation against DWR

import os
import math
import datetime
import numpy
import collections

import matplotlib
from matplotlib.backends.backend_agg import \
                 FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import cartopy
import cartopy.crs as ccrs

import Meteorographica.weathermap as wm
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
         default=("%s/images/DWR/vcs_20CR3_1953_reliability+error" % 
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

# Get the DWR observations within +- 15 hours
obs=DWR.load_observations('prmsl',
                          dte-datetime.timedelta(hours=15),
                          dte+datetime.timedelta(hours=15))
# Remove stations already in ISPD
obs=obs[~obs['name'].isin(['LERWICK','STORNOWAY','VALENTIA',
                           'CULDROSE','GORLESTON','LEUCHARS'])]
# sort them from north to south
obs=obs.sort_values(by='latitude',ascending=True)
# Get the list of stations - preserving order
stations=collections.OrderedDict.fromkeys(obs.loc[:,'name']).keys()

# Add the observations from 20CR
obs_t=twcr.load_observations_fortime(dte,version='4.5.1')
# Filter to those assimilated and near the UK
obs_s=obs_t.loc[((obs_t['Latitude']>0) & 
                   (obs_t['Latitude']<90)) &
                ((obs_t['Longitude']>240) | 
                   (obs_t['Longitude']<100))].copy()

# load the pressures
prmsl=twcr.load('prmsl',args.year,args.month,args.day,args.hour,
                             version='4.5.1')
prmsl.data=prmsl.data/100.0

# UK-centred projection
projection=ccrs.RotatedPole(pole_longitude=177.5, 
                            pole_latitude=35.5)
scale=20
extent=[scale*-1*aspect/2-5,scale*aspect/2-5,scale*-1,scale]

# Contour plot on the left
ax_map=fig.add_axes([0.01,0.01,0.485,0.98],projection=projection)

local_plots.plot_contour(ax_map,extent,dte,prmsl,obs_t,obs,
                         projection=projection,
                         stations=stations)

# Label with the date
wm.plot_label(ax_map,
              '%04d-%02d-%02d:%02d' % (args.year,args.month,
                                          args.day,args.hour),
              facecolor=fig.get_facecolor(),
              x_fraction=0.02,
              horizontalalignment='left')

# obs_v_reanalysis scatter plot top right
ax_ovr=fig.add_axes([0.54,0.55,0.45,0.44])

local_plots.plot_rotated_scatter(ax_ovr,prmsl,obs,dte)
                   
# deviation_v_spread scatter plot bottom right
ax_dvs=fig.add_axes([0.54,0.06,0.45,0.44])

local_plots.plot_deviation_spread(ax_dvs,prmsl,obs,dte)
 
# Output as png
fig.savefig('%s/reliability+error_%04d%02d%02d%02d%02d.png' % 
                                      (args.opdir,args.year,
                                       args.month,args.day,
                                      int(args.hour),
                                      int(args.hour%1*60)))
