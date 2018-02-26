# UK region 20Cr2c spaghetti-contour prmsl map
# Use Meteorographica weathermap functions

import math
import datetime
import numpy

import iris
import iris.analysis

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import cartopy
import cartopy.crs as ccrs

import Meteorographica.weathermap as wm
import Meteorographica.data.cera20c as cera20c

import DWR

# Date to show
year=1903
month=10
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
scale=20
extent=[scale*-1*math.sqrt(2),scale*math.sqrt(2),scale*-1,scale]

# Single plot filling the figure
ax_20C=fig.add_axes([0,0,1,1],projection=projection)
ax_20C.set_axis_off()
ax_20C.set_extent(extent, crs=projection)

# Background, grid, and land
ax_20C.background_patch.set_facecolor((0.88,0.88,0.88,1))
wm.add_grid(ax_20C)
land_img_20C=ax_20C.background_img(name='GreyT', resolution='low')

# load the pressures
prmsl=cera20c.get_slice_at_hour('prmsl',year,month,day,hour)

# For each ensemble member, make a contour plot
for m in prmsl.coord('member').points:
    prmsl_e=prmsl.extract(iris.Constraint(member=m))
    prmsl_e.data=prmsl_e.data/100 # To hPa
    CS=wm.plot_contour(ax_20C,prmsl_e,
                   levels=numpy.arange(870,1050,10),
                   colors='blue',
                   label=False,
                   linewidths=0.5)

# Add the ensemble mean - with labels
prmsl_m=prmsl.collapsed('member', iris.analysis.MEAN)
prmsl_m.data=prmsl_m.data/100 # To hPa
prmsl_s=prmsl.collapsed('member', iris.analysis.STD_DEV)
prmsl_s.data=prmsl_s.data/100
# Mask out mean where uncertainties large
prmsl_m.data[numpy.where(prmsl_s.data>3)]=numpy.nan
CS=wm.plot_contour(ax_20C,prmsl_m,
                   levels=numpy.arange(870,1050,10),
                   colors='black',
                   label=True,
                   linewidths=2)

wm.plot_label(ax_20C,'%04d-%02d-%02d:%02d' % (year,month,day,hour),
                     facecolor=fig.get_facecolor())
# Output as png
fig.savefig('Spaghetti_prmsl_%04d%02d%02d%02d_cera.png' % (year,month,day,hour))
