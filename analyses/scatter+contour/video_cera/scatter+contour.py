#!/bin/env python

# UK region weather plot 
# CERA20C pressures and validation against DWR

import os
import math
import datetime
import numpy
import collections
import random

import iris
import iris.analysis

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle

import cartopy
import cartopy.crs as ccrs

import Meteorographica.weathermap as wm
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
                    default="%s/images/DWR/scatter+contour.cera" % os.getenv('SCRATCH'),
                    type=str,required=False)
args = parser.parse_args()
if not os.path.isdir(args.opdir):
    os.makedirs(args.opdir)
 
dte=datetime.datetime(args.year,args.month,args.day,
                      int(args.hour),int(args.hour%1*60))

# Get the station list and order
obs_month=DWR.get_obs(datetime.datetime(1903,10,1,1),
                datetime.datetime(1903,10,31,23),
                'prmsl')
# sort them from north to south
obs_month=obs_month.sort_values(by='latitude',ascending=True)
# Get the list of stations - preserving order
stations=collections.OrderedDict.fromkeys(obs_month.loc[:,'name']).keys()
# Get the locations for all the stations
latlon={}
for station in stations:
    latlon[station]=DWR.get_station_location(obs_month,station)

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

# UK-centred projection
projection=ccrs.RotatedPole(pole_longitude=177.5, pole_latitude=35.5)
scale=20
extent=[scale*-1*aspect/2-5,scale*aspect/2-5,scale*-1,scale]

# Contour plot on the left
ax_map=fig.add_axes([0.01,0.01,0.485,0.98],projection=projection)
ax_map.set_axis_off()
ax_map.set_extent(extent, crs=projection)

# Background, grid and land 
ax_map.background_patch.set_facecolor((0.88,0.88,0.88,1))
wm.add_grid(ax_map)
land_img_20C=ax_map.background_img(name='GreyT', resolution='low')

# Mark all the stations used in the month - empty circle
wm.plot_obs(ax_map,obs_month,lat_label='latitude',
            lon_label='longitude',radius=0.15,facecolor=(1,0,0,0))

# Get the DWR observations within +- 15 hours
obs=DWR.get_obs(dte-datetime.timedelta(hours=15.1),
                dte+datetime.timedelta(hours=15.1),
                'prmsl')

# Mark all the stations used in this day - filled circle
wm.plot_obs(ax_map,obs,lat_label='latitude',
            lon_label='longitude',radius=0.15,facecolor='red')

# load the pressures
prmsl=cera20c.get_slice_at_hour('prmsl',args.year,args.month,args.day,args.hour)

# For each ensemble member, make a contour plot
for m in prmsl.coord('member').points:
    prmsl_e=prmsl.extract(iris.Constraint(member=m))
    prmsl_e.data=prmsl_e.data/100 # To hPa
    CS=wm.plot_contour(ax_map,prmsl_e,
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
CS=wm.plot_contour(ax_map,prmsl_m,
                   levels=numpy.arange(870,1050,10),
                   colors='black',
                   label=True,
                   linewidths=2)

# Label with the date
wm.plot_label(ax_map,'%04d-%02d-%02d:%02d' % (args.year,args.month,args.day,int(args.hour)),
                     facecolor=fig.get_facecolor(),
                     x_fraction=0.02,
                     horizontalalignment='left')

# Validation scatterplot on the right
ax_scp=fig.add_axes([0.6,0.03,0.39,0.96])

# pressure range
extent=[945,1045]

# x-axis
ax_scp.set_xlim(extent)

# y-axis
ax_scp.set_ylim([1,len(stations)+1])
y_locations=[x+0.5 for x in range(1,len(stations)+1)]
ax_scp.yaxis.set_major_locator(matplotlib.ticker.FixedLocator(y_locations))
ax_scp.yaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(
                              [DWR.pretty_name(s) for s in stations]))

# Custom grid spacing
for y in range(0,len(stations)):
    ax_scp.add_line(matplotlib.lines.Line2D(
            xdata=(extent[0],extent[1]), ydata=(y+1.5,y+1.5),
            linestyle='solid',
            linewidth=0.2,
            color=(0.5,0.5,0.5,1),
            zorder=0))

# Get a pressure interpolated to the selected time for each station
interpolated={}
for station in stations:
    try:
        interpolated[station]=DWR.at_station_and_time(obs,station,dte)
    except StandardError:
        interpolated[station]=None

# Plot the station pressures
for y in range(0,len(stations)):
    station=stations[y]
    if interpolated[station] is None:
        continue
    mslp=interpolated[station]
    ax_scp.add_line(matplotlib.lines.Line2D(
            xdata=(mslp,mslp), ydata=(y+1.25,y+1.75),
            linestyle='solid',
            linewidth=4,
            color=(1,0,0,1),
            zorder=1))
    
# for each station, plot the reanalysis ensemble at that station
interpolator = iris.analysis.Linear().interpolator(prmsl, 
                                                   ['latitude', 'longitude'])
for y in range(0,len(stations)):
    station=stations[y]
    ensemble=interpolator([latlon[station]['latitude'],
                           latlon[station]['longitude']])
    for m in range(0,len(ensemble.data)):
        ax_scp.add_patch(Circle((ensemble.data[m]/100,
                                (y+1.25+m*1.0/(2*len(ensemble.data)))),
                            radius=0.1,
                            facecolor='blue',
                            edgecolor='blue',
                            alpha=0.5,
                            zorder=0.5))

# Join each station name to its location on the map
# Need another axes, filling the whole fig
ax_full=fig.add_axes([0,0,1,1])
ax_full.patch.set_alpha(0.0)  # Transparent background

# Map location of a station in ax_full coordinates
def pos_left(obs,stations,idx):
    station=stations[idx]
    rp=ax_map.projection.transform_points(ccrs.PlateCarree(),
                              numpy.asarray(latlon[station]['longitude']),
                              numpy.asarray(latlon[station]['latitude']))
    new_lon=rp[:,0]
    new_lat=rp[:,1]

    result={}
    result['x']=0.01+0.485*((new_lon-(scale*-1*aspect/2)+5)/(scale*2*aspect/2))
    result['y']=0.01+0.98*((new_lat-(scale*-1))/(scale*2))
    return result

# Label location of a station in ax_full coordinates
def pos_right(obs,stations,idx):
    result={}
    result['x']=0.51
    result['y']=0.03+(0.96/len(stations))*(idx+0.5)
    return result

for i in range(0,len(stations)):
    p_left=pos_left(obs,stations,i)
    p_right=pos_right(obs,stations,i)
    ax_full.add_patch(Circle((p_right['x'],
                              p_right['y']),
                             radius=0.001,
                             facecolor=(1,0,0,1),
                             edgecolor=(0,0,0,1),
                             alpha=1,
                             zorder=1))
    ax_full.add_line(matplotlib.lines.Line2D(
            xdata=(p_left['x'],p_right['x']),
            ydata=(p_left['y'],p_right['y']),
            linestyle='solid',
            linewidth=0.2,
            color=(1,0,0,0.5),
            zorder=1))

# Output as png
fig.savefig('%s/Scatter+contour_%04d%02d%02d%02d%02d.png' % 
                                      (args.opdir,args.year,
                                       args.month,args.day,
                                      int(args.hour),
                                      int(args.hour%1*60)))
