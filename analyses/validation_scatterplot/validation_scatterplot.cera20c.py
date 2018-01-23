# DWR observations and CERA20C ensemble

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

import Meteorographica.data.cera20c as cera20c

import DWR

# Date to show - Heroy hurricane
year=1901
month=1
day=22
hour=18
dte=datetime.datetime(year,month,day,hour)

# Get the DWR observations within +- 6 hours
obs=DWR.get_obs(dte-datetime.timedelta(hours=12.1),
                dte+datetime.timedelta(hours=12.1),
                'prmsl')
# sort them from north to south
obs=obs.sort_values(by='latitude',ascending=True)
# Get the list of stations - preserving order
stations=collections.OrderedDict.fromkeys(obs.loc[:,'name']).keys()

# Get the observation at the station interpolated to the desired time
#  when this works - move it to the DWR module.
def dwr_at_station_and_time(obs,station,dte):
    at_station=obs.loc[obs['name']==station]
    if at_station.empty:
        raise StandardError('No data for station %s' % station)
    at_station=at_station.sort_values(by='dtm',ascending=True)
    hit=at_station.loc[at_station['dtm']==dte]
    if not hit.empty:
        return hit['value'].values[0]
    before=at_station.loc[at_station['dtm']<dte]
    if before.empty:
        raise StandardError('No data for station %s before %s' % (station,
                     dte.strftime("%Y-%m-%d:%H:%M")))
    before=before.iloc[-1] # last row
    after=at_station.loc[at_station['dtm']>dte]
    if after.empty:
        raise StandardError('No data for station %s after %s' % (station,
                     dte.strftime("%Y-%m-%d:%H:%M")))
    after=after.iloc[0] # first row
    weight=((dte-before['dtm']).total_seconds()/
           (after['dtm']-before['dtm']).total_seconds())
    return after['value']*weight+before['value']*(1-weight)

# Get the position of a named station
def get_station_location(obs,station):
    at_station=obs.loc[obs['name']==station]
    if at_station.empty:
        raise StandardError('No data for station %s' % station)
    result={'latitude': at_station['latitude'].values[0],
            'longitude':at_station['longitude'].values[0]}
    return result

# Portrait page
fig=Figure(figsize=(22/math.sqrt(2),22),  # Width, Height (inches)
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

# pressure range
extent=[945,1045]

# Single plot filling the figure
ax=fig.add_axes([0.15,0.05,0.84,0.94])

# x-axis
ax.set_xlim(extent)
ax.set_xlabel('MSLP (hPa)')

# y-axis
ax.set_ylim([1,len(stations)+1])
y_locations=[x+0.5 for x in range(1,len(stations)+1)]
ax.yaxis.set_major_locator(matplotlib.ticker.FixedLocator(y_locations))
ax.yaxis.set_major_formatter(matplotlib.ticker.FixedFormatter((stations)))
ax.set_xlabel('MSLP (hPa)')

# Custom grid spacing
for y in range(0,len(stations)):
    ax.add_line(matplotlib.lines.Line2D(
            xdata=(extent[0],extent[1]), ydata=(y+1.5,y+1.5),
            linestyle='solid',
            linewidth=0.2,
            color=(0.5,0.5,0.5,1),
            zorder=0))

# Get a pressure interpolated to the selected time for each station
interpolated={}
for station in stations:
    try:
        interpolated[station]=dwr_at_station_and_time(obs,station,dte)
    except StandardError:
        interpolated[station]=None

# Plot the station pressures
for y in range(0,len(stations)):
    station=stations[y]
    if interpolated[station] is None:
        continue
    mslp=interpolated[station]
    ax.add_line(matplotlib.lines.Line2D(
            xdata=(mslp,mslp), ydata=(y+1.25,y+1.75),
            linestyle='solid',
            linewidth=4,
            color=(1,0,0,1),
            zorder=1))
    
# load the reanalysis pressures 
prmsl=cera20c.get_slice_at_hour('prmsl',year,month,day,hour)

# for each station, plot the reanalysis ensemble at that station
interpolator = iris.analysis.Linear().interpolator(prmsl, 
                                                   ['latitude', 'longitude'])
for y in range(0,len(stations)):
    station=stations[y]
    latlon=get_station_location(obs,station)
    ensemble=interpolator([latlon['latitude'],latlon['longitude']])
    for m in range(0,len(ensemble.data)):
        ax.add_patch(Circle((ensemble.data[m]/100,
                             random.uniform(y+1.25,y+1.75)),
                            radius=0.1,
                            facecolor='blue',
                            edgecolor='blue',
                            alpha=0.5,
                            zorder=0.5))

# Output as png
fig.savefig('DWR_v_20CR_%04d%02d%02d%02d.cera20c.png' % (year,month,day,hour))
