# UK region weather plot 
# 20CR3 pressures and validation against DWR

import math
import datetime

import matplotlib
from matplotlib.backends.backend_agg import \
                 FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import Meteorographica.data.twcr as twcr

import DWR

import local_plots
 
# Date to show 
year=1953
month=2
day=10
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
obs=obs[~obs['name'].isin(['LERWICK','STORNOWAY','VALENTIA',
                           'CULDROSE','GORLESTON','LEUCHARS'])]
# sort them from north to south
obs=obs.sort_values(by='latitude',ascending=True)

# Get the reanalysis pressures and observations
prmsl=twcr.load('prmsl',year,month,day,hour,
                             version='4.5.1')
prmsl.data=prmsl.data/100  #] convert to hPa
obs_t=twcr.load_observations_fortime(dte,version='4.5.1')
# Filter to those near the UK # For speed only, optional
obs_t=obs_t.loc[((obs_t['Latitude']>0) & 
                   (obs_t['Latitude']<90)) &
                ((obs_t['Longitude']>240) | 
                   (obs_t['Longitude']<100))].copy()

local_plots.plot_scatter_contour(fig,prmsl,obs_t,obs,dte)

# Output as png
fig.savefig('Scatter+contour_%04d%02d%02d%02d.png' % 
                                    (year,month,day,hour))
