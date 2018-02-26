# UK region weather plot from 20CR2C
# Use Meteorographica weathermap functions

import math
import datetime

import matplotlib

from matplotlib.backends.backend_agg \
           import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import cartopy
import cartopy.crs as ccrs

import Meteorographica.weathermap as wm
import Meteorographica.data.twcr as twcr

import DWR
 
# Date to show - Heroy hurricane
year=1901
month=1
day=22
hour=18
dte=datetime.datetime(year,month,day,hour)

# Landscape page
fig=Figure(figsize=(22,22/math.sqrt(2)),  # Width, Height (inches)
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
scale=10
extent=[scale*-1,scale,scale*-1*math.sqrt(2),scale*math.sqrt(2)]

# Two side-by-side plots
ax_20C=fig.add_axes([0.01,0.01,0.485,0.98],projection=projection)
ax_20C.set_axis_off()
ax_20C.set_extent(extent, crs=projection)
ax_DWR=fig.add_axes([0.505,0.01,0.485,0.98],projection=projection)
ax_DWR.set_axis_off()
ax_DWR.set_extent(extent, crs=projection)

# Background, grid and land for both
ax_20C.background_patch.set_facecolor((0.88,0.88,0.88,1))
ax_DWR.background_patch.set_facecolor((0.88,0.88,0.88,1))
wm.add_grid(ax_20C)
wm.add_grid(ax_DWR)
land_img_20C=ax_20C.background_img(name='GreyT', resolution='low')
land_img_DWR=ax_DWR.background_img(name='GreyT', resolution='low')

# 20CR2c data
wm.plot_label(ax_20C,'Observations in 20CR 2c',
                     facecolor=fig.get_facecolor())
# Add the observations
obs=twcr.get_obs(dte-datetime.timedelta(hours=24),dte,'3.5.1')
# Filter to those assimilated and near the UK
obs_s=obs.loc[(obs['Assimilation.indicator']==1) &
              ((obs['Latitude']>0) & 
                  (obs['Latitude']<90)) &
              ((obs['Longitude']>240) | 
                 (obs['Longitude']<100))].copy()
wm.plot_obs(ax_20C,obs_s,radius=0.15)

# DWR data
obs=DWR.get_obs(dte-datetime.timedelta(hours=24),dte,'prmsl')
wm.plot_obs(ax_DWR,obs,lat_label='latitude',
            lon_label='longitude',radius=0.15)
wm.plot_label(ax_DWR,'Observations in DWR',
                     facecolor=fig.get_facecolor())

# Output as png
fig.savefig('Coverage.png')
