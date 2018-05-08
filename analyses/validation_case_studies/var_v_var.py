
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

# Fill the frame with an axes
ax=fig.add_axes([0.08,0.08,0.89,0.89])

ipfile=("%s/images/DWR/vcs_cera20c_1903_month_comparison.pkl" %
                os.getenv('SCRATCH'))
d_file = open(ipfile, 'rb')
dmonth = pickle.load(d_file)
d_file.close()
local_plots.plot_vvv(ax,dmonth)

ipfile=("%s/images/DWR/vcs_cera20c_1953_month_comparison.pkl" %
                os.getenv('SCRATCH'))
d_file = open(ipfile, 'rb')
dmonth = pickle.load(d_file)
d_file.close()
local_plots.plot_vvv(ax,dmonth,obs_errors=None,point_color=(.5,.5,1))

ipfile=("%s/images/DWR/vcs_20CR2c_1903_month_comparison.pkl" %
                os.getenv('SCRATCH'))
d_file = open(ipfile, 'rb')
dmonth = pickle.load(d_file)
d_file.close()
local_plots.plot_vvv(ax,dmonth,obs_errors=None,point_color='black')

ipfile=("%s/images/DWR/vcs_20CR2c_1953_month_comparison.pkl" %
                os.getenv('SCRATCH'))
d_file = open(ipfile, 'rb')
dmonth = pickle.load(d_file)
d_file.close()
local_plots.plot_vvv(ax,dmonth,obs_errors=None,point_color=(.5,.5,.5))

ipfile=("%s/images/DWR/vcs_20CR3_1903_month_comparison.pkl" %
                os.getenv('SCRATCH'))
d_file = open(ipfile, 'rb')
dmonth = pickle.load(d_file)
d_file.close()
local_plots.plot_vvv(ax,dmonth,obs_errors=None,point_color='red')

ipfile=("%s/images/DWR/vcs_20CR3_1953_month_comparison.pkl" %
                os.getenv('SCRATCH'))
d_file = open(ipfile, 'rb')
dmonth = pickle.load(d_file)
d_file.close()
local_plots.plot_vvv(ax,dmonth,obs_errors=None,point_color=(1,.5,.5))

# Output as png
fig.savefig('V_v_V.png')

