# UK region weather plot 
# 20CR2c pressures and validation against DWR

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

# UK-centred projection
projection=ccrs.RotatedPole(pole_longitude=177.5, pole_latitude=35.5)
scale=20
extent=[scale*-1,scale,scale*-1*math.sqrt(2),scale*math.sqrt(2)]

# Contour plot on the left
ax_map=fig.add_axes([0.01,0.01,0.485,0.98],projection=projection)
ax_map.set_axis_off()
ax_map.set_extent(extent, crs=projection)

# Background, grid and land 
ax_map.background_patch.set_facecolor((0.88,0.88,0.88,1))
wm.add_grid(ax_map)
land_img_20C=ax_map.background_img(name='GreyT', resolution='low')

# Get the DWR observations within +- 12 hours
obs=DWR.load_observations('prmsl',
                          dte-datetime.timedelta(hours=12),
                          dte+datetime.timedelta(hours=12))
# Remove stations already in ISPD
obs=obs[~obs['name'].isin(['LERWICK','STORNOWAY','VALENTIA',
                           'CULDROSE','GORLESTON','LEUCHARS'])]
# sort them from north to south
obs=obs.sort_values(by='latitude',ascending=True)
# Get the list of stations - preserving order
stations=collections.OrderedDict.fromkeys(obs.loc[:,'name']).keys()

wm.plot_obs(ax_map,obs,lat_label='latitude',
            lon_label='longitude',radius=0.25,facecolor='red',edgecolor='red')

# Add the observations from 20CR
obs_t=twcr.load_observations_fortime(dte,version='4.5.1')
# Filter to those assimilated and near the UK
obs_s=obs_t.loc[((obs_t['Latitude']>0) & 
                   (obs_t['Latitude']<90)) &
              ((obs_t['Longitude']>240) | 
                   (obs_t['Longitude']<100))].copy()
wm.plot_obs(ax_map,obs_s,radius=0.15)

# load the pressures
prmsl=twcr.load('prmsl',year,month,day,hour,
                             version='4.5.1')

# For each ensemble member, make a contour plot
for m in prmsl.coord('member').points:
    prmsl_e=prmsl.extract(iris.Constraint(member=m))
    prmsl_e.data=prmsl_e.data/100 # To hPa
    CS=wm.plot_contour(ax_map,prmsl_e,
                   levels=numpy.arange(870,1050,10),
                   colors='blue',
                   label=False,
                   linewidths=0.1)

# Add the ensemble mean - with labels
prmsl_m=prmsl.collapsed('member', iris.analysis.MEAN)
prmsl_m.data=prmsl_m.data/100 # To hPa
prmsl_s=prmsl.collapsed('member', iris.analysis.STD_DEV)
prmsl_s.data=prmsl_s.data/100
# Mask out mean where uncertainties large
prmsl_m.data[numpy.where(prmsl_s.data>3)]=numpy.nan
CS=wm.plot_contour(ax_map,prmsl_m,
                   levels=numpy.arange(870,1050,10),
                   colors='black',
                   label=True,
                   linewidths=2)

# Label with the date
wm.plot_label(ax_map,
              '%04d-%02d-%02d:%02d' % (year,month,day,hour),
              facecolor=fig.get_facecolor(),
              x_fraction=0.02,
              horizontalalignment='left')

# Get a pressure interpolated to the selected time for each station
interpolated={}
for station in stations:
    try:
        interpolated[station]=DWR.at_station_and_time(
                                          obs,station,dte)
    except StandardError:
        interpolated[station]=None
# Get the data at station locations

# Get the reanalysis ensemble at the station locations
ensemble={}
interpolator = iris.analysis.Linear().interpolator(prmsl, 
                                   ['latitude', 'longitude'])
for station in stations:
    latlon=DWR.get_station_location(obs,station)
    ensemble[station]=interpolator([latlon['latitude'],
                                    latlon['longitude']]).data

# obs_v_reanalysis scatter plot top right
ax_ovr=fig.add_axes([0.54,0.54,0.45,0.45])

# pressure range
extent=[965,1045]

# x & y-axis
ax_ovr.set_xlim(extent)
ax_ovr.set_xlabel('Observed MSLP (hPa)')
ax_ovr.set_ylim(-7.5,7.5)
ax_ovr.set_ylabel('Ensemble-Observed MSLP (hPa)')

# Background 1-to-1 line
ax_ovr.add_line(matplotlib.lines.Line2D(
            xdata=extent, ydata=(0,0),
            linestyle='solid',
            linewidth=1,
            color=(0.5,0.5,0.5,1),
            zorder=1))

# Plot the ensembles
for station in stations:
    if interpolated[station] is None: continue
    obs_ens=[interpolated[station]]*len(ensemble[station])
    ens_dif=[ensemble[station][i]/100.0-obs_ens[i] for i in range(len(obs_ens))]
    ax_ovr.scatter(obs_ens,
                   ens_dif,
                   s=10,
                   marker='o',
                   c='blue',
                   linewidths=0.1,
                   edgecolors='blue')
                   
# deviation_v_spread scatter plot bottom right
ax_dvs=fig.add_axes([0.54,0.04,0.45,0.45])

# pressure range
extent=[-7.5,7.5]

# x & y-axis
ax_dvs.set_xlim(extent)
ax_dvs.set_xlabel('Observation-ensemble mean (hPa)')
ax_dvs.set_ylim(0,extent[1])
ax_dvs.set_ylabel('Ensemble standard deviation (hPa)')

# Ensemble means
ensm={}
for station in stations:
    ensm[station]=numpy.mean(ensemble[station])

# Expected ensemble sd assuming obs have 2hpa error
exp_x=numpy.arange(extent[0],extent[1],0.01)
exp_y=numpy.sqrt(numpy.maximum(exp_x**2-4,0))
ax_dvs.add_line(matplotlib.lines.Line2D(
            xdata=exp_x, ydata=exp_y,
            linestyle='solid',
            linewidth=1,
            color=(0.5,0.5,0.5,1),
            zorder=1))

# Plot the ensembles
for station in stations:
    if interpolated[station] is None: continue
    ax_dvs.scatter(ensm[station]/100.0-interpolated[station],
                   numpy.std(ensemble[station])/100.0,
                   s=30,
                   marker='o',
                   c='black',
                   linewidths=0.1,
                   edgecolors='black')
 
# Output as png
fig.savefig('reliability+error_%04d%02d%02d%02d.png' % 
                                    (year,month,day,hour))
