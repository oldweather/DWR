
import os
import pickle

import matplotlib
from matplotlib.backends.backend_agg import \
                 FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import local_plots

# Landscape page
fig=Figure(figsize=(11,11),  # Width, Height (inches)
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

# load the pre-prepared data
ipfile=("%s/images/DWR/vcs_20CR2c_1953_month_comparison.pkl" %
                os.getenv('SCRATCH'))
d_file = open(ipfile, 'rb')
dmonth = pickle.load(d_file)
d_file.close()

# Fill the frame with an axes
ax=fig.add_axes([0.08,0.08,0.89,0.89])

local_plots.plot_eve(ax,dmonth)

# Output as png
fig.savefig('E_v_E.png')

