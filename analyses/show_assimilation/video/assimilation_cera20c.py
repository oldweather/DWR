#!/bin/env python

# UK region weather plot 
# Effect of assimilation on CERA20C

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
import DIYA

# Get the number of stations to assimilate from the command line
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--count", help="Year",
                    type=float,required=True)
parser.add_argument("--opdir", help="Directory for output files",
                    default="%s/images/DWR/assimilate.cera" % os.getenv('SCRATCH'))
args = parser.parse_args()
if not os.path.isdir(args.opdir):
    os.makedirs(args.opdir)

 
# Date to show - Heroy hurricane
year=1901
month=1
day=22
hour=18
dte=datetime.datetime(year,month,day,hour)

# Landscape page
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

# Get the DWR observations within +- 0.5 hours
obs=DWR.get_obs(dte-datetime.timedelta(hours=0.5),
                dte+datetime.timedelta(hours=0.5),
                'prmsl')
# sort them from north to south
obs=obs.sort_values(by='latitude',ascending=True)
# Get the list of stations - preserving order
stations=collections.OrderedDict.fromkeys(obs.loc[:,'name']).keys()

# load the pressures
prmsl=cera20c.get_slice_at_hour('prmsl',year,month,day,hour)

# List of stations to assimilate
if int(args.count)==0:
    prmsl2=prmsl
    to_assimilate=stations[0]
else:
    to_assimilate=stations[:int(args.count):1]
    obs_assimilate=obs[obs.name.isin(to_assimilate)]
    obs_assimilate.value=obs_assimilate.value*100 # to Pa
    prmsl2=DIYA.constrain_cube(prmsl,prmsl,obs=obs_assimilate,obs_error=25)
prmsl3=prmsl2
if args.count>int(args.count): 
    to_assimilate=stations[:int(args.count)+1:1]
    obs_assimilate=obs[obs.name.isin(to_assimilate)]
    obs_assimilate.value=obs_assimilate.value*100 # to Pa
    prmsl3=DIYA.constrain_cube(prmsl,prmsl,obs=obs_assimilate,obs_error=25)
    frac=args.count-int(args.count)
    prmsl2.data=prmsl2.data*(1-frac)+prmsl3.data*frac

if len(to_assimilate)>0:
   wm.plot_obs(ax_map,obs_assimilate,lat_label='latitude',
               lon_label='longitude',radius=0.15,facecolor='yellow')
if len(to_assimilate)<len(stations):
   obs_left=obs[~obs.name.isin(to_assimilate)]
   wm.plot_obs(ax_map,obs_left,lat_label='latitude',
               lon_label='longitude',radius=0.15,facecolor='black')
   
# Pre-assimilation contour plot
for m in range(1, 10):   # Same number as CERA
    prmsl_e=prmsl.extract(iris.Constraint(member=m))
    prmsl_e.data=prmsl_e.data/100 # To hPa
    CS=wm.plot_contour(ax_map,prmsl_e,
                   levels=numpy.arange(870,1050,10),
                   colors='red',
                   label=False,
                   linewidths=0.2)


# For each ensemble member, make a contour plot
#for m in prmsl.coord('member').points:
for m in range(1, 10):   # Same number as CERA
    prmsl_e=prmsl2.extract(iris.Constraint(member=m))
    prmsl_e.data=prmsl_e.data/100 # To hPa
    CS=wm.plot_contour(ax_map,prmsl_e,
                   levels=numpy.arange(870,1050,10),
                   colors='blue',
                   label=False,
                   linewidths=0.3)

# Add the ensemble mean - with labels
prmsl_m=prmsl2.collapsed('member', iris.analysis.MEAN)
prmsl_m.data=prmsl_m.data/100 # To hPa
prmsl_s=prmsl2.collapsed('member', iris.analysis.STD_DEV)
prmsl_s.data=prmsl_s.data/100
# Mask out mean where uncertainties large
prmsl_m.data[numpy.where(prmsl_s.data>3)]=numpy.nan
CS=wm.plot_contour(ax_map,prmsl_m,
                   levels=numpy.arange(870,1050,10),
                   colors='black',
                   label=True,
                   linewidths=2)

# Label with the date
wm.plot_label(ax_map,'%04d-%02d-%02d:%02d' % (year,month,day,hour),
                     facecolor=fig.get_facecolor(),
                     x_fraction=0.02,
                     horizontalalignment='left')

# Validation scatterplot on the right
ax_scp=fig.add_axes([0.6,0.04,0.39,0.95])

# pressure range
extent=[945,1045]

# x-axis
ax_scp.set_xlim(extent)
ax_scp.set_xlabel('MSLP (hPa)')

# y-axis
ax_scp.set_ylim([1,len(stations)+1])
y_locations=[x+0.5 for x in range(1,len(stations)+1)]
ax_scp.yaxis.set_major_locator(matplotlib.ticker.FixedLocator(y_locations))
ax_scp.yaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(
                              [DWR.pretty_name(s) for s in stations]))
ax_scp.set_xlabel('MSLP (hPa)')

# Custom grid spacing
for y in range(0,len(stations)):
    ax_scp.add_line(matplotlib.lines.Line2D(
            xdata=(extent[0],extent[1]), ydata=(y+1.5,y+1.5),
            linestyle='solid',
            linewidth=0.2,
            color=(0.5,0.5,0.5,1),
            zorder=0))

# Plot the station pressures
for y in range(0,len(stations)):
    station=stations[y]
    mslp=obs[obs.name==station].value.values[0]
    ax_scp.add_line(matplotlib.lines.Line2D(
            xdata=(mslp,mslp), ydata=(y+1.25,y+1.75),
            linestyle='solid',
            linewidth=3,
            color=(0,0,0,1),
            zorder=1))
    
# for each station, plot the reanalysis ensemble at that station
# both before and after assimilation
interpolator = iris.analysis.Linear().interpolator(prmsl, 
                                                   ['latitude', 'longitude'])
for y in range(0,len(stations)):
    station=stations[y]
    latlon=DWR.get_station_location(obs,station)
    ensemble=interpolator([latlon['latitude'],latlon['longitude']])
    for m in range(0,len(ensemble.data)):
        ax_scp.add_patch(Circle((ensemble.data[m]/100,
                            random.uniform(y+1.25,y+1.75)),
                            radius=0.1,
                            facecolor='red',
                            edgecolor='red',
                            alpha=0.5,
                            zorder=0.5))
interpolator = iris.analysis.Linear().interpolator(prmsl2, 
                                                   ['latitude', 'longitude'])
for y in range(0,len(stations)):
    station=stations[y]
    latlon=DWR.get_station_location(obs,station)
    ensemble=interpolator([latlon['latitude'],latlon['longitude']])
    for m in range(0,len(ensemble.data)):
        ax_scp.add_patch(Circle((ensemble.data[m]/100,
                            random.uniform(y+1.25,y+1.75)),
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
    latlon=DWR.get_station_location(obs,stations[idx])
    rp=ax_map.projection.transform_points(ccrs.PlateCarree(),
                                          numpy.asarray(latlon['longitude']),
                                          numpy.asarray(latlon['latitude']))
    new_lon=rp[:,0]
    new_lat=rp[:,1]

    result={}
    result['x']=0.01+0.485*((new_lon-(scale*-1))/(scale*2))
    result['y']=0.01+0.98*((new_lat-(scale*math.sqrt(2)*-1))/(scale*2*math.sqrt(2)))
    return result

# Label location of a station in ax_full coordinates
def pos_right(obs,stations,idx):
    result={}
    result['x']=0.51
    result['y']=0.04+(0.95/len(stations))*(idx+0.5)
    return result

for i in range(0,len(stations)):
    p_left=pos_left(obs,stations,i)
    p_right=pos_right(obs,stations,i)
    pcol='black'
    if stations[i] in to_assimilate: pcol='yellow'
    ax_full.add_patch(Circle((p_right['x'],
                              p_right['y']),
                             radius=0.003,
                             facecolor=pcol,
                             edgecolor='black',
                             alpha=1,
                             zorder=1))
    ax_full.add_line(matplotlib.lines.Line2D(
            xdata=(p_left['x'],p_right['x']),
            ydata=(p_left['y'],p_right['y']),
            linestyle='solid',
            linewidth=0.2,
            color=(0,0,0,0.5),
            zorder=1))

# Output as png
fig.savefig('%s/Assimilated.cera20c.%02d.%03d.png' % (args.opdir,
                           int(args.count),int((args.count-int(args.count))*100)))
