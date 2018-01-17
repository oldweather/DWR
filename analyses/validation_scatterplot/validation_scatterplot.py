# DWR observations and 20CR2c ensemble

import math
import datetime
import numpy

import iris
import iris.analysis

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import Meteorographica.data.twcr as twcr

import DWR

# Date to show - Heroy hurricane
year=1901
month=1
day=22
hour=6
dte=datetime.datetime(year,month,day,hour)

# Portrait page
fig=Figure(figsize=(22/math.sqrt(2),22),  # Width, Height (inches)
           dpi=100,
           facecolor=(0.88,0.88,0.88,1),
           edgecolor=None,
           linewidth=0.0,
           frameon=False,
           subplotpars=None,
           tight_layout=None)
canvas=FigureCanvas(fig)

# Ranges - pressure and no. of stations
extent=[970,1030,0,50]

# Single plot filling the figure
ax_20C=fig.add_axes([0,0,1,1])
#ax_20C.set_extent(extent)

# Background
#ax_20C.background_patch.set_facecolor((0.88,0.88,0.88,1))

# Get the DWR observations within +- 6 hours
obs=DWR.get_obs(dte-datetime.timedelta(hours=6),
                dte+datetime.timedelta(hours=6),
                'prmsl')
# Get the list of stations
stations=set(obs.loc[:,'name'])
# Get a pressure interpolated to the selected time for each station
interpolated={}
for station in stations:
   rows = obs.where(name=station)


# load the reanalysis pressures 
prmsl=twcr.get_slice_at_hour('prmsl',year,month,day,hour,
                             version='3.5.1',type='ensemble')

# Output as png
fig.savefig('DWR_v_20CR_%04d%02d%02d%02d.png' % (year,month,day,hour))
