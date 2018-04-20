# UK region weather plot 
# 20CR3 pressures and validation against DWR

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
# Filter to those near the UK
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
#for m in range(1, 10):   # Same number as CERA
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

# Validation scatterplot on the right
ax_scp=fig.add_axes([0.6,0.04,0.39,0.95])

# pressure range
extent=[945,1045]

# x-axis
ax_scp.set_xlim(extent)
ax_scp.set_xlabel('MSLP (hPa)')

# y-axis
ax_scp.set_ylim([1,len(stations)+1])
y_locations=[x+0.5 for x in range(1,len(stations)+1)]
ax_scp.yaxis.set_major_locator(
              matplotlib.ticker.FixedLocator(y_locations))
ax_scp.yaxis.set_major_formatter(
              matplotlib.ticker.FixedFormatter(
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
        interpolated[station]=DWR.at_station_and_time(
                                          obs,station,dte)
    except StandardError:
        interpolated[station]=None

# Plot the station pressures
for y in range(0,len(stations)):
    station=stations[y]
    if interpolated[station] is None:
        continue
    mslp=interpolated[station]
    ax_scp.add_line(matplotlib.lines.Line2D(
            xdata=(mslp,mslp), ydata=(y+1.25,y+1.75),
            linestyle='solid',
            linewidth=4,
            color=(1,0,0,1),
            zorder=1))
    
# for each station, plot the reanalysis ensemble at that station
interpolator = iris.analysis.Linear().interpolator(prmsl, 
                                   ['latitude', 'longitude'])
for y in range(0,len(stations)):
    station=stations[y]
    latlon=DWR.get_station_location(obs,station)
    ensemble=interpolator([latlon['latitude'],
                           latlon['longitude']])
    ax_scp.scatter(ensemble.data/100,
                numpy.random.uniform(low=y+1.25,
                                     high=y+1.75,
                                     size=len(ensemble.data)),
                25, # Point size
                'blue', # Color
                marker='.',
                edgecolors='face',
                linewidths=0.0,
                alpha=0.5,
                zorder=0.5)

# Join each station name to its location on the map
# Need another axes, filling the whole fig
ax_full=fig.add_axes([0,0,1,1])
ax_full.patch.set_alpha(0.0)  # Transparent background

# Map location of a station in ax_full coordinates
def pos_left(obs,stations,idx):
    latlon=DWR.get_station_location(obs,stations[idx])
    rp=ax_map.projection.transform_points(ccrs.PlateCarree(),
                              numpy.asarray(latlon['longitude']),
                              numpy.asarray(latlon['latitude']))
    new_lon=rp[:,0]
    new_lat=rp[:,1]

    result={}
    result['x']=0.01+0.485*((new_lon-(scale*-1))/(scale*2))
    result['y']=0.01+0.98*((new_lat-(scale*math.sqrt(2)*-1))/
                                       (scale*2*math.sqrt(2)))
    return result

# Label location of a station in ax_full coordinates
def pos_right(obs,stations,idx):
    result={}
    result['x']=0.51
    result['y']=0.04+(0.95/len(stations))*(idx+0.5)
    return result

for i in range(0,len(stations)):
    p_left=pos_left(obs,stations,i)
    p_right=pos_right(obs,stations,i)
    ax_full.add_patch(Circle((p_right['x'],
                              p_right['y']),
                             radius=0.001,
                             facecolor=(1,0,0,1),
                             edgecolor=(0,0,0,1),
                             alpha=1,
                             zorder=1))
    ax_full.add_line(matplotlib.lines.Line2D(
            xdata=(p_left['x'],p_right['x']),
            ydata=(p_left['y'],p_right['y']),
            linestyle='solid',
            linewidth=0.2,
            color=(1,0,0,0.5),
            zorder=1))

# Output as png
fig.savefig('Scatter+contour_%04d%02d%02d%02d.png' % 
                                    (year,month,day,hour))