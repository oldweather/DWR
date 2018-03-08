# Show effect of assimilating Fort William observation

import math
import datetime
import numpy
import pandas

import iris
import iris.analysis

import matplotlib
from matplotlib.backends.backend_agg import \
             FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import cartopy
import cartopy.crs as ccrs

import Meteorographica.weathermap as wm
import Meteorographica.data.cera20c as cera20c

import DIYA
RANDOM_SEED = 5

# Date to show
year=1903
month=2
day=27
hour=6
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
scale=12
extent=[scale*-1,scale,scale*-1*math.sqrt(2),scale*math.sqrt(2)]

# Two side-by-side plots
ax_20C=fig.add_axes([0.01,0.01,0.485,0.98],projection=projection)
ax_20C.set_axis_off()
ax_20C.set_extent(extent, crs=projection)
ax_wFW=fig.add_axes([0.505,0.01,0.485,0.98],projection=projection)
ax_wFW.set_axis_off()
ax_wFW.set_extent(extent, crs=projection)

# Background, grid and land for both
ax_20C.background_patch.set_facecolor((0.88,0.88,0.88,1))
ax_wFW.background_patch.set_facecolor((0.88,0.88,0.88,1))
wm.add_grid(ax_20C)
wm.add_grid(ax_wFW)
land_img_20C=ax_20C.background_img(name='GreyT', resolution='low')
land_img_DWR=ax_wFW.background_img(name='GreyT', resolution='low')

# CERA data
prmsl=cera20c.load('prmsl',year,month,day,hour)

# For each ensemble member, make a contour plot
for m in prmsl.coord('member').points:
    prmsl_e=prmsl.extract(iris.Constraint(member=m))
    prmsl_e.data=prmsl_e.data/100 # To hPa
    CS=wm.plot_contour(ax_20C,prmsl_e,
                   levels=numpy.arange(870,1050,10),
                   colors='blue',
                   label=False,
                   linewidths=0.3)

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

wm.plot_label(ax_20C,'CERA-20C',
                     fontsize=16,
                     facecolor=fig.get_facecolor(),
                     x_fraction=0.02,
                     horizontalalignment='left')

# Get the Fort William ob
station_lat=56.82
station_lon= -5.1
FW_data=pandas.read_table('FW_pressure_Feb_1903.dat',
                          header=None,
                          delim_whitespace=True)
i_day=day
i_hour=hour
if hour==0:
    i_day=i_day-1
    i_hour=24
FW_ob=FW_data.iloc[i_day-1,i_hour+2]*100
obs_assimilate=pandas.DataFrame(data={'year': year, 'month': month, 'day': day,
                                      'hour': hour, 'minute': 0,
                                      'latitude': station_lat,
                                      'longitude': station_lon,
                                      'value': FW_ob, 'name': 'Fort William'},
                                       index=[0])
obs_assimilate=obs_assimilate.assign(dtm=pandas.to_datetime(
                   obs_assimilate[['year','month','day','hour','minute']]))

# Update mslp by assimilating Fort William ob.
prmsl2=DIYA.constrain_cube(prmsl,prmsl,obs=obs_assimilate,obs_error=10,
                           random_state=RANDOM_SEED,lat_range=(20,85),lon_range=(280,60))

# Plot the Fort William ob
wm.plot_obs(ax_wFW,obs_assimilate,lat_label='latitude',
            lon_label='longitude',radius=0.1,facecolor='red')

# For each ensemble member, make a contour plot
for m in prmsl2.coord('member').points:
    prmsl_e=prmsl2.extract(iris.Constraint(member=m))
    prmsl_e.data=prmsl_e.data/100 # To hPa
    CS=wm.plot_contour(ax_wFW,prmsl_e,
                   levels=numpy.arange(870,1050,10),
                   colors='blue',
                   label=False,
                   linewidths=0.3)

# Add the ensemble mean - with labels
prmsl_m=prmsl2.collapsed('member', iris.analysis.MEAN)
prmsl_m.data=prmsl_m.data/100 # To hPa
prmsl_s=prmsl2.collapsed('member', iris.analysis.STD_DEV)
prmsl_s.data=prmsl_s.data/100
# Mask out mean where uncertainties large
prmsl_m.data[numpy.where(prmsl_s.data>3)]=numpy.nan
CS=wm.plot_contour(ax_wFW,prmsl_m,
                   levels=numpy.arange(870,1050,10),
                   colors='black',
                   label=True,
                   linewidths=2)

wm.plot_label(ax_wFW,'With Fort William observation',
                     fontsize=16,
                     facecolor=fig.get_facecolor(),
                     x_fraction=0.02,
                     horizontalalignment='left')

wm.plot_label(ax_wFW,
              '%04d-%02d-%02d:%02d' % (year,month,day,hour),
              fontsize=16,
              facecolor=fig.get_facecolor(),
              x_fraction=0.98,
              horizontalalignment='right')

# Output as png
fig.savefig('Add_FW_CERA_%04d%02d%02d%02d.png' % 
                                  (year,month,day,hour))
