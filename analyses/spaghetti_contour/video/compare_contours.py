#!/bin/env python

# UK region weather plot 
# Compare pressures from 20CR and CERA20C
# Video version

import os
import math
import datetime
import numpy

import iris
import iris.analysis

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import cartopy
import cartopy.crs as ccrs

import Meteorographica.weathermap as wm
import Meteorographica.data.twcr as twcr
import Meteorographica.data.cera20c as cera20c

import DWR

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
                    default="%s/images/DWR/compare_contours" % os.getenv('SCRATCH'),
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

# UK-centred projection
projection=ccrs.RotatedPole(pole_longitude=177.5, pole_latitude=35.5)
scale=20
extent=[scale*-1*aspect/2,scale*aspect/2,scale*-1,scale]

# Two side-by-side plots
ax_20C=fig.add_axes([0.01,0.01,0.485,0.98],projection=projection)
ax_20C.set_axis_off()
ax_20C.set_extent(extent, crs=projection)
ax_C2C=fig.add_axes([0.505,0.01,0.485,0.98],projection=projection)
ax_C2C.set_axis_off()
ax_C2C.set_extent(extent, crs=projection)

# Background, grid and land for both
ax_20C.background_patch.set_facecolor((0.88,0.88,0.88,1))
ax_C2C.background_patch.set_facecolor((0.88,0.88,0.88,1))
wm.add_grid(ax_20C)
wm.add_grid(ax_C2C)
land_img_20C=ax_20C.background_img(name='GreyT', resolution='low')
land_img_DWR=ax_C2C.background_img(name='GreyT', resolution='low')

# 20CR2c data
obs=DWR.get_obs(dte-datetime.timedelta(hours=24),dte,'prmsl')
wm.plot_obs(ax_20C,obs,lat_label='latitude',
            lon_label='longitude',radius=0.15,facecolor='red')

# Add the observations from 20CR
obs=twcr.get_obs(dte-datetime.timedelta(hours=24),dte,'3.5.1')
# Filter to those assimilated and near the UK
obs_s=obs.loc[(obs['Assimilation.indicator']==1) &
              ((obs['Latitude']>0) & (obs['Latitude']<90)) &
              ((obs['Longitude']>240) | (obs['Longitude']<100))].copy()
wm.plot_obs(ax_20C,obs_s,radius=0.15)

# load the pressures
prmsl=twcr.get_slice_at_hour('prmsl',args.year,args.month,args.day,
                             args.hour,version='3.5.1',type='ensemble')

# For each ensemble member, make a contour plot
#for m in prmsl.coord('member').points:
for m in range(1, 10):   # Same number as CERA
    prmsl_e=prmsl.extract(iris.Constraint(member=m))
    prmsl_e.data=prmsl_e.data/100 # To hPa
    CS=wm.plot_contour(ax_20C,prmsl_e,
                   levels=numpy.arange(870,1050,10),
                   colors='blue',
                   label=False,
                   linewidths=0.3)

# Add the ensemble mean - with labels
prmsl_m=prmsl.collapsed('member', iris.analysis.MEAN)
prmsl_m.data=prmsl_m.data/100 # To hPa
prmsl_s=prmsl.collapsed('member', iris.analysis.STD_DEV)
prmsl_s.data=prmsl_s.data/100
# Mask out mean where uncertainties large
prmsl_m.data[numpy.where(prmsl_s.data>3)]=numpy.nan
CS=wm.plot_contour(ax_20C,prmsl_m,
                   levels=numpy.arange(870,1050,10),
                   colors='black',
                   label=False,
                   linewidths=2)

# 20CR2c observations
wm.plot_label(ax_20C,'20CR2c (members 1-10)',
                     facecolor=fig.get_facecolor(),
                     x_fraction=0.02,
                     horizontalalignment='left')

# CERA data
obs=DWR.get_obs(dte-datetime.timedelta(hours=24),dte,'prmsl')
wm.plot_obs(ax_C2C,obs,lat_label='latitude',
            lon_label='longitude',radius=0.15,facecolor='red')

# load the pressures
prmsl=cera20c.get_slice_at_hour('prmsl',args.year,args.month,
                                args.day,args.hour,
                                type='ensemble')

# For each ensemble member, make a contour plot
for m in prmsl.coord('member').points:
    prmsl_e=prmsl.extract(iris.Constraint(member=m))
    prmsl_e.data=prmsl_e.data/100 # To hPa
    CS=wm.plot_contour(ax_C2C,prmsl_e,
                   levels=numpy.arange(870,1050,10),
                   colors='blue',
                   label=False,
                   linewidths=0.3)

# Add the ensemble mean - with labels
prmsl_m=prmsl.collapsed('member', iris.analysis.MEAN)
prmsl_m.data=prmsl_m.data/100 # To hPa
prmsl_s=prmsl.collapsed('member', iris.analysis.STD_DEV)
prmsl_s.data=prmsl_s.data/100
# Mask out mean where uncertainties large
prmsl_m.data[numpy.where(prmsl_s.data>3)]=numpy.nan
CS=wm.plot_contour(ax_C2C,prmsl_m,
                   levels=numpy.arange(870,1050,10),
                   colors='black',
                   label=False,
                   linewidths=2)

wm.plot_label(ax_C2C,'CERA20C',
                     facecolor=fig.get_facecolor(),
                     x_fraction=0.02,
                     horizontalalignment='left')

wm.plot_label(ax_C2C,'%04d-%02d-%02d:%02d' % (args.year,args.month,
                                              args.day,int(args.hour)),
                     facecolor=fig.get_facecolor(),
                     x_fraction=0.98,
                     horizontalalignment='right')

# Output as png
fig.savefig('%s/Compare_mslp_%04d%02d%02d%02d%02d.png' % 
                      (args.opdir,args.year,args.month,args.day,
                       int(args.hour),int(args.hour%1*60)))
