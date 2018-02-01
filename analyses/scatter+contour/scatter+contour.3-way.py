# UK region weather plot 
# 3-way comparison pressures and validation against DWR

import math
import datetime
import numpy
import collections
import random

import iris
import iris.analysis

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle

import cartopy
import cartopy.crs as ccrs

import Meteorographica.weathermap as wm
import Meteorographica.data.twcr as twcr
import Meteorographica.data.cera20c as cera20c

import DWR
 
# Date to show 
year=1901
month=1
day=22
hour=18
dte=datetime.datetime(year,month,day,hour)

# Landscape page
fig=Figure(figsize=(22,22*math.sqrt(2)),  # Width, Height (inches)
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

# V3 Contour plot on the top left
ax_map_V3=fig.add_axes([0.01,0.505,0.485,0.49],projection=projection)
ax_map_V3.set_axis_off()
ax_map_V3.set_extent(extent, crs=projection)

# Background, grid and land 
ax_map_V3.background_patch.set_facecolor((0.88,0.88,0.88,1))
wm.add_grid(ax_map_V3)
land_img_20C=ax_map_V3.background_img(name='GreyT', resolution='low')

# CERA Contour plot on the bottom right
ax_map_CER=fig.add_axes([0.505,0.01,0.485,0.49],projection=projection)
ax_map_CER.set_axis_off()
ax_map_CER.set_extent(extent, crs=projection)

# Background, grid and land 
ax_map_CER.background_patch.set_facecolor((0.88,0.88,0.88,1))
wm.add_grid(ax_map_CER)
land_img_20C=ax_map_CER.background_img(name='GreyT', resolution='low')

# V2c Contour plot on the bottom left
ax_map_V2c=fig.add_axes([0.01,0.01,0.485,0.49],projection=projection)
ax_map_V2c.set_axis_off()
ax_map_V2c.set_extent(extent, crs=projection)

# Background, grid and land 
ax_map_V2c.background_patch.set_facecolor((0.88,0.88,0.88,1))
wm.add_grid(ax_map_V2c)
land_img_20C=ax_map_V2c.background_img(name='GreyT', resolution='low')

# Get the DWR observations within +- 15 hours
obs=DWR.get_obs(dte-datetime.timedelta(hours=15.1),
                dte+datetime.timedelta(hours=15.1),
                'prmsl')
# sort them from north to south
obs=obs.sort_values(by='latitude',ascending=True)
# Get the list of stations - preserving order
#stations=collections.OrderedDict.fromkeys(obs.loc[:,'name']).keys()
# Selected subset of stations
stations=['PORTADELGADA', 'PERPIGNAN', 'BIARRITZ', 'LYONS', 'BELFORT', 'MUNICH', 'PARIS', 'JERSEY', 'SCILLY', 'FRANKFURT', 'PORTLANDBILL', 'CAPGRISNEZ', 'PEMBROKE', 'OXFORD', 'ROCHESPOINT', 'BERLIN', 'YARMOUTH', 'THEHELDER', 'PARSONSTOWN', 'LIVERPOOL', 'SPURNHEAD', 'CUXHAVEN', 'BLACKSODPOINT', 'DONAGHADEE', 'SHIELDS', 'MALINHEAD', 'FANO', 'LEITH', 'FORTWILLIAM',  'WISBY', 'SKAGEN', 'STORNOWAY', 'WICK', 'FAERDER', 'SKUDESNAES', 'KARLSTAD',  'SUMBURGHHEAD', 'HERNOSAND', 'CHRISTIANSUND', 'BODO']
obs=obs[obs.name.isin(stations)]

wm.plot_obs(ax_map_V3,obs,lat_label='latitude',
            lon_label='longitude',radius=0.15,facecolor='black')
wm.plot_obs(ax_map_V2c,obs,lat_label='latitude',
            lon_label='longitude',radius=0.15,facecolor='black')
wm.plot_obs(ax_map_CER,obs,lat_label='latitude',
            lon_label='longitude',radius=0.15,facecolor='black')

# V3

# load the pressures
prmsl=twcr.get_slice_at_hour('prmsl',year,month,day,hour,
                             version='4.5.1',type='ensemble')

# For each ensemble member, make a contour plot
#for m in prmsl.coord('member').points:
for m in range(1, 10):   # Same number as V2
    prmsl_e=prmsl.extract(iris.Constraint(member=m))
    prmsl_e.data=prmsl_e.data/100 # To hPa
    CS=wm.plot_contour(ax_map_V3,prmsl_e,
                   levels=numpy.arange(870,1060,10),
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
CS=wm.plot_contour(ax_map_V3,prmsl_m,
                   levels=numpy.arange(870,1060,10),
                   colors='black',
                   label=True,
                   linewidths=2)

# V2c

# load the pressures
prmsl=twcr.get_slice_at_hour('prmsl',year,month,day,hour,
                             version='3.5.1',type='ensemble')
# For each ensemble member, make a contour plot
#for m in prmsl.coord('member').points:
for m in range(1, 10):   # Same number as V2
    prmsl_e=prmsl.extract(iris.Constraint(member=m))
    prmsl_e.data=prmsl_e.data/100 # To hPa
    CS=wm.plot_contour(ax_map_V2c,prmsl_e,
                   levels=numpy.arange(870,1060,10),
                   colors='red',
                   label=False,
                   linewidths=0.5)

# Add the ensemble mean - with labels
prmsl_m=prmsl.collapsed('member', iris.analysis.MEAN)
prmsl_m.data=prmsl_m.data/100 # To hPa
prmsl_s=prmsl.collapsed('member', iris.analysis.STD_DEV)
prmsl_s.data=prmsl_s.data/100
# Mask out mean where uncertainties large
prmsl_m.data[numpy.where(prmsl_s.data>3)]=numpy.nan
CS=wm.plot_contour(ax_map_V2c,prmsl_m,
                   levels=numpy.arange(870,1060,10),
                   colors='black',
                   label=True,
                   linewidths=2)
# CERA
# load the pressures
prmsl=cera20c.get_slice_at_hour('prmsl',year,month,day,hour)
# For each ensemble member, make a contour plot
for m in range(1, 10):
    prmsl_e=prmsl.extract(iris.Constraint(member=m))
    prmsl_e.data=prmsl_e.data/100 # To hPa
    CS=wm.plot_contour(ax_map_CER,prmsl_e,
                   levels=numpy.arange(870,1060,10),
                   colors='green', #wm.rgb_to_hex((0,1,0,1)),# (0.76,0.88,0.29,1),
                   label=False,
                   linewidths=0.5)

# Add the ensemble mean - with labels
prmsl_m=prmsl.collapsed('member', iris.analysis.MEAN)
prmsl_m.data=prmsl_m.data/100 # To hPa
prmsl_s=prmsl.collapsed('member', iris.analysis.STD_DEV)
prmsl_s.data=prmsl_s.data/100
# Mask out mean where uncertainties large
prmsl_m.data[numpy.where(prmsl_s.data>3)]=numpy.nan
CS=wm.plot_contour(ax_map_CER,prmsl_m,
                   levels=numpy.arange(870,1060,10),
                   colors='black',
                   label=True,
                   linewidths=2)

# Label with the date
wm.plot_label(ax_map_V2c,'%04d-%02d-%02d:%02d' % (year,month,day,hour),
                     facecolor=fig.get_facecolor(),
                     x_fraction=0.02,
                     horizontalalignment='left')

# Validation scatterplot on the top right
ax_scp=fig.add_axes([0.6,0.54,0.39,0.45])

# pressure range
extent=[945,1045]

# x-axis
ax_scp.set_xlim(extent)
ax_scp.set_xlabel('MSLP (hPa)')

# y-axis
ax_scp.set_ylim([1,len(stations)+1])
y_locations=[x+0.5 for x in range(1,len(stations)+1)]
ax_scp.yaxis.set_major_locator(matplotlib.ticker.FixedLocator(y_locations))
ax_scp.yaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(
                              [DWR.pretty_name(s) for s in stations]))
ax_scp.set_xlabel('MSLP (hPa)')

# Custom grid spacing
for y in range(0,len(stations)):
    ax_scp.add_line(matplotlib.lines.Line2D(
            xdata=(extent[0],extent[1]), ydata=(y+1.5,y+1.5),
            linestyle='solid',
            linewidth=0.2,
            color=(0.5,0.5,0.5,1),
            zorder=0))

# Get a pressure interpolated to the selected time for each station
interpolated={}
for station in stations:
    try:
        interpolated[station]=DWR.at_station_and_time(obs,station,dte)
    except StandardError:
        interpolated[station]=None

# Plot the station pressures
for y in range(0,len(stations)):
    station=stations[y]
    if interpolated[station] is None:
        continue
    mslp=interpolated[station]
    ax_scp.add_line(matplotlib.lines.Line2D(
            xdata=(mslp,mslp), ydata=(y+1.1,y+1.9),
            linestyle='solid',
            linewidth=4,
            color=(0,0,0,1),
            zorder=1))
    
# for each station, plot the reanalysis ensemble at that station
prmsl=twcr.get_slice_at_hour('prmsl',year,month,day,hour,
                             version='4.5.1',type='ensemble')
interpolator = iris.analysis.Linear().interpolator(prmsl, 
                                                   ['latitude', 'longitude'])
for y in range(0,len(stations)):
    station=stations[y]
    latlon=DWR.get_station_location(obs,station)
    ensemble=interpolator([latlon['latitude'],latlon['longitude']])
    for m in range(0,len(ensemble.data)):
        ax_scp.add_patch(Circle((ensemble.data[m]/100,
                            random.uniform(y+1.6,y+1.9)),
                            radius=0.05,
                            facecolor='blue',
                            edgecolor='blue',
                            alpha=0.5,
                            zorder=0.5))
prmsl=twcr.get_slice_at_hour('prmsl',year,month,day,hour,
                             version='3.5.1',type='ensemble')
interpolator = iris.analysis.Linear().interpolator(prmsl, 
                                                   ['latitude', 'longitude'])
for y in range(0,len(stations)):
    station=stations[y]
    latlon=DWR.get_station_location(obs,station)
    ensemble=interpolator([latlon['latitude'],latlon['longitude']])
    for m in range(0,len(ensemble.data)):
        ax_scp.add_patch(Circle((ensemble.data[m]/100,
                            random.uniform(y+1.4,y+1.7)),
                            radius=0.05,
                            facecolor='red',
                            edgecolor='red',
                            alpha=0.5,
                            zorder=0.5))
prmsl=cera20c.get_slice_at_hour('prmsl',year,month,day,hour)
interpolator = iris.analysis.Linear().interpolator(prmsl, 
                                                   ['latitude', 'longitude'])
for y in range(0,len(stations)):
    station=stations[y]
    latlon=DWR.get_station_location(obs,station)
    ensemble=interpolator([latlon['latitude'],latlon['longitude']])
    for m in range(0,len(ensemble.data)):
        ax_scp.add_patch(Circle((ensemble.data[m]/100,
                            random.uniform(y+1.1,y+1.4)),
                            radius=0.1,
                            facecolor='green',
                            edgecolor='green',
                            alpha=0.5,
                            zorder=0.5))


# Join each station name to its location on the map
# Need another axes, filling the whole fig
ax_full=fig.add_axes([0,0,1,1])
ax_full.patch.set_alpha(0.0)  # Transparent background

# Map location of a station in ax_full coordinates
def pos_left(obs,stations,idx):
    latlon=DWR.get_station_location(obs,stations[idx])
    rp=ax_map_V3.projection.transform_points(ccrs.PlateCarree(),
                                          numpy.asarray(latlon['longitude']),
                                          numpy.asarray(latlon['latitude']))
    new_lon=rp[:,0]
    new_lat=rp[:,1]

    result={}
    result['x']=0.01+0.485*((new_lon-(scale*-1))/(scale*2))
    result['y']=0.505+0.49*((new_lat-(scale*math.sqrt(2)*-1))/(scale*2*math.sqrt(2)))
    return result

# Label location of a station in ax_full coordinates
def pos_right(obs,stations,idx):
    result={}
    result['x']=0.51
    result['y']=0.54+(0.45/len(stations))*(idx+0.5)
    return result

for i in range(0,len(stations)):
    p_left=pos_left(obs,stations,i)
    p_right=pos_right(obs,stations,i)
    ax_full.add_patch(Circle((p_right['x'],
                              p_right['y']),
                             radius=0.001,
                             facecolor=(0,0,0,1),
                             edgecolor=(0,0,0,1),
                             alpha=1,
                             zorder=1))
    ax_full.add_line(matplotlib.lines.Line2D(
            xdata=(p_left['x'],p_right['x']),
            ydata=(p_left['y'],p_right['y']),
            linestyle='solid',
            linewidth=0.2,
            color=(0,0,0,0.5),
            zorder=1))

# Output as png
fig.savefig('Scatter+contour_%04d%02d%02d%02d.3way.png' % 
                                      (year,month,day,hour))
