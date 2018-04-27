# UK region weather plot 
# 20CR2c pressures and validation against DWR

import os
import math
import pickle
import numpy

import matplotlib
from matplotlib.backends.backend_agg import \
                 FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

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

# load the pre-prepared data
ipfile=("%s/images/DWR/vcs_20CR2c_1903_month_comparison.pkl" %
                os.getenv('SCRATCH'))
d_file = open(ipfile, 'rb')
dmonth = pickle.load(d_file)
d_file.close()

# Fill the frame with an axes
ax=fig.add_axes([0.05,0.05,0.93,0.93])

d_range=[965,1040]

# x-axis
ax.set_xlim(d_range)
ax.set_xlabel('Observed MSLP (hPa)')
# y-axis
ax.set_ylim(d_range)
ax.set_ylabel('Ensemble MSLP (hPa)')

# Background 1-to-1 line
ax.add_line(matplotlib.lines.Line2D(
            xdata=[d_range],
            ydata=[d_range],
            linestyle='solid',
            linewidth=1,
            color=(0.5,0.5,0.5,1),
            zorder=1))

# Plot the ensembles
for idx in range(len(dmonth['observations'])):
    ax.scatter(dmonth['observations'][idx],
               numpy.mean(dmonth['ensembles'][idx][0]),
               s=100,
               marker='.',
               alpha=1.0,
               linewidths=0.01,
               c='blue',
               edgecolors='blue')

# Output as png
fig.savefig('Scatter_month_ensm.png')

