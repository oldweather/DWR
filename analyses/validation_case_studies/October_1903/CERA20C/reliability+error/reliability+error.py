# UK region weather plot 
# CERA20C pressures and validation against DWR

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
import Meteorographica.data.cera20c as cera20c

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

# load the pressures
prmsl=cera20c.load('prmsl',year,month,day,hour)
prmsl.data=prmsl.data/100.0 # To hPa

# Contour plot on the left
projection=ccrs.RotatedPole(pole_longitude=177.5, pole_latitude=35.5)
ax_map=fig.add_axes([0.01,0.01,0.485,0.98],projection=projection)
scale=20
extent=[scale*-1,scale,scale*-1*math.sqrt(2),scale*math.sqrt(2)]

local_plots.plot_contour(ax_map,extent,dte,prmsl,None,obs,
                         projection=projection,
                         contour_width=0.3)

# Label with the date
wm.plot_label(ax_map,
              '%04d-%02d-%02d:%02d' % (year,month,day,hour),
              facecolor=fig.get_facecolor(),
              x_fraction=0.02,
              horizontalalignment='left')

# obs_v_reanalysis scatter plot top right
ax_ovr=fig.add_axes([0.54,0.54,0.45,0.45])

local_plots.plot_rotated_scatter(ax_ovr,prmsl,obs,dte)

                  
# deviation_v_spread scatter plot bottom right
ax_dvs=fig.add_axes([0.54,0.04,0.45,0.45])

local_plots.plot_deviation_spread(ax_dvs,prmsl,obs,dte)
 
# Output as png
fig.savefig('reliability+error_%04d%02d%02d%02d.png' % 
                                    (year,month,day,hour))
