# UK region weather plot 
# 20CR2c and 3 DWR validation

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
 
# Date to show 
year=1903
month=10
day=25
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
font = {'family' : 'sans-serif',
        'sans-serif' : 'Arial',
        'weight' : 'normal',
        'size'   : 16}
matplotlib.rc('font', **font)

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
# load the pressures
prmsl=twcr.load('prmsl',year,month,day,hour,
                             version='2c')
prmsl.data=prmsl.data/100.0 # To hPa

# Contour plot on the left
projection=ccrs.RotatedPole(pole_longitude=177.5, pole_latitude=35.5)
ax_map=fig.add_axes([0.01,0.01,0.485,0.98],projection=projection)
scale=20
extent=[scale*-1,scale,scale*-1*math.sqrt(2),scale*math.sqrt(2)]

local_plots.plot_contour(ax_map,extent,dte,prmsl,obs_t,obs,
                         projection=projection)

# Label with the date
wm.plot_label(ax_map,'v2c',
              facecolor=fig.get_facecolor(),
              x_fraction=0.02,
              fontsize=16,
              horizontalalignment='left')

# overlay obs_v_reanalysis scatter plot top left
ax_ovr=fig.add_axes([0.05,0.79,0.25,0.16])

local_plots.plot_rotated_scatter(ax_ovr,prmsl,obs,dte)

# Get the observations from 20CR3
obs_t=twcr.load_observations_fortime(dte,version='4.5.1')
# Filter to those near the UK
obs_s=obs_t.loc[((obs_t['Latitude']>0) & 
                   (obs_t['Latitude']<90)) &
                ((obs_t['Longitude']>240) | 
                   (obs_t['Longitude']<100))].copy()
# load the pressures
prmsl=twcr.load('prmsl',year,month,day,hour,
                             version='4.5.1')
prmsl.data=prmsl.data/100.0 # To hPa

# Contour plot on the right
ax_map3=fig.add_axes([0.51,0.01,0.485,0.98],projection=projection)
scale=20
extent=[scale*-1,scale,scale*-1*math.sqrt(2),scale*math.sqrt(2)]

local_plots.plot_contour(ax_map3,extent,dte,prmsl,obs_t,obs,
                         projection=projection,
                         n_contours=56)

# Label with the version
wm.plot_label(ax_map3,'v3',
              facecolor=fig.get_facecolor(),
              x_fraction=0.02,
              fontsize=16,
              horizontalalignment='left')
# Label with the date
wm.plot_label(ax_map3,
              '%04d-%02d-%02d:%02d' % (year,month,day,hour),
              facecolor=fig.get_facecolor(),
              x_fraction=0.98,
              fontsize=16,
              horizontalalignment='right')

# overlay obs_v_reanalysis scatter plot top left
ax_ovr3=fig.add_axes([0.55,0.79,0.25,0.16])

local_plots.plot_rotated_scatter(ax_ovr3,prmsl,obs,dte)
                 
 
# Output as png
fig.savefig('comparison_%04d%02d%02d%02d.png' % 
                                    (year,month,day,hour))
