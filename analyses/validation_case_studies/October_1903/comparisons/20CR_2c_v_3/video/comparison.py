#!/bin/env python

# UK region weather plot 
# 20CR2c and 3 DWR validation

import os
import os.path
import math
import datetime
import numpy
import collections

import iris
import iris.analysis

import matplotlib
from matplotlib.backends.backend_agg import \
                 FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle

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
           default=("%s/images/DWR/vcs_20CR_comparison_1903" % 
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
                          datetime.datetime(1903,10,1,0),
                          datetime.datetime(1903,10,31,23))
# Remove stations already in ISPD
obs=obs[~obs['name'].isin(['BODO','HAPARANDA','HERNOSAND',
                           'STOCKHOLM','WISBY','ABERDEEN',
                           'VALENCIA','FANO','SCILLY','JERSEY',
                           'LISBON','DUNGENESS','THEHELDER',
                           'BERLIN'])]
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
obs=obs[~obs['name'].isin(['BODO','HAPARANDA','HERNOSAND',
                           'STOCKHOLM','WISBY','ABERDEEN',
                           'VALENCIA','FANO','SCILLY','JERSEY',
                           'LISBON','DUNGENESS','THEHELDER',
                           'BERLIN'])]

# Get the observations from 20CR2c
obs_t=twcr.load_observations_fortime(dte,version='2c')
# Filter to those near the UK
obs_s=obs_t.loc[((obs_t['Latitude']>0) & 
                   (obs_t['Latitude']<90)) &
                ((obs_t['Longitude']>240) | 
                   (obs_t['Longitude']<100))].copy()
# Get the reanalysis pressures
prmsl=twcr.load('prmsl',args.year,args.month,args.day,
                             args.hour,version='2c')
prmsl.data=prmsl.data/100.0 # To hPa

# Contour plot on the left
projection=ccrs.RotatedPole(pole_longitude=177.5, pole_latitude=35.5)
ax_map=fig.add_axes([0.01,0.01,0.485,0.98],projection=projection)
scale=20
aspect=fig.get_size_inches()[1]/(fig.get_size_inches()[0]/2.0)
extent=[scale*-1,scale,scale*-1*aspect,scale*aspect]

local_plots.plot_contour(ax_map,extent,dte,prmsl,obs_t,obs,
                         projection=projection,
                         stations=stations,
                         station_latlon=latlon,
                         label_mean_contour=False)

# Label with the version
wm.plot_label(ax_map,'v2c',
              facecolor=fig.get_facecolor(),
              x_fraction=0.02,
              fontsize=16,
              horizontalalignment='left')

# overlay obs_v_reanalysis scatter plot top left
ax_ovr=fig.add_axes([0.05,0.79,0.25,0.16])

local_plots.plot_rotated_scatter(ax_ovr,prmsl,obs,dte,
                                 y_label='Ensemble-Observed (hPa)')

# Get the observations from 20CR3
obs_t=twcr.load_observations_fortime(dte,version='4.5.1')
# Filter to those near the UK
obs_s=obs_t.loc[((obs_t['Latitude']>0) & 
                   (obs_t['Latitude']<90)) &
                ((obs_t['Longitude']>240) | 
                   (obs_t['Longitude']<100))].copy()
# load the pressures
prmsl=twcr.load('prmsl',args.year,args.month,args.day,
                             args.hour,version='4.5.1')
prmsl.data=prmsl.data/100.0 # To hPa

# Contour plot on the right
ax_map3=fig.add_axes([0.51,0.01,0.485,0.98],projection=projection)

local_plots.plot_contour(ax_map3,extent,dte,prmsl,obs_t,obs,
                         projection=projection,
                         n_contours=56,
                         stations=stations,
                         station_latlon=latlon,
                         label_mean_contour=False)

# Label with the version
wm.plot_label(ax_map3,'v3',
              facecolor=fig.get_facecolor(),
              x_fraction=0.02,
              fontsize=16,
              horizontalalignment='left')
# Label with the date
wm.plot_label(ax_map3,
              '%04d-%02d-%02d:%02d' % (args.year,args.month,
                                       args.day,args.hour),
              facecolor=fig.get_facecolor(),
              x_fraction=0.98,
              fontsize=16,
              horizontalalignment='right')

# overlay obs_v_reanalysis scatter plot top left
ax_ovr3=fig.add_axes([0.55,0.79,0.25,0.16])

local_plots.plot_rotated_scatter(ax_ovr3,prmsl,obs,dte,
                                 y_label='Ensemble-Observed (hPa)')
                 
 
# Output as png
fig.savefig('%s/comparison_%04d%02d%02d%02d%02d.png' % 
                                      (args.opdir,args.year,
                                       args.month,args.day,
                                      int(args.hour),
                                      int(args.hour%1*60)))
