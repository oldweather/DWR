# UK region weather plot 
# CERA20C pressures and validation against DWR

import math
import datetime

import matplotlib
from matplotlib.backends.backend_agg import \
                 FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

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
# sort them from north to south
obs=obs.sort_values(by='latitude',ascending=True)

# Get the reanalysis pressures
prmsl=cera20c.load('prmsl',year,month,day,hour)
prmsl.data=prmsl.data/100  # convert to hPa

local_plots.plot_scatter_contour(fig,prmsl,None,obs,dte,
                                 scatter_point_size=100,
                                 contour_width=0.3)

# Output as png
fig.savefig('Scatter+contour_%04d%02d%02d%02d.png' % 
                                    (year,month,day,hour))
