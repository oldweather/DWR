# (C) British Crown Copyright 2017, Met Office
#
# This code is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#

# Combination scatter+contour plot

import iris
import DWR
import numpy
import collections
import matplotlib
from matplotlib.patches import Circle
import cartopy
import cartopy.crs as ccrs
import Meteorographica.weathermap as wm

from scatter import plot_scatter
from contour import plot_contour

def plot_scatter_contour(fig,field,obs_r,dwr_obs,dte,
                         projection=ccrs.RotatedPole(pole_longitude=177.5,
                                         pole_latitude=35.5),
                         scale=20,
                         pressure_range=[945,1045]):
    """Make a combined contour -plot and scatter plot

    Args:
        fig (:`matplotlib.figure`): Figure to hold the plot
        field (:obj:`iris.Cube.cube`): Reanalysis mslp ensemble
        obs_r (:obj:`pandas.DataFrame`): Reanalysis observations.
        dwr_obs (:obj:`pandas.DataFrame`): DWR observations.
        dte (:obj:`datetime.datetime`): Time of data to plot

    |
    """

    ax_map=fig.add_axes([0.01,0.01,0.485,0.98],projection=projection)
    aspect=fig.get_size_inches()[1]/(fig.get_size_inches()[0]/2.0)
    extent=[scale*-1,scale,scale*-1*aspect,scale*aspect]
    stations=collections.OrderedDict.fromkeys(
                     dwr_obs.loc[:,'name']).keys()

    plot_contour(ax_map,extent,dte,field,obs_r,dwr_obs)

    # Label with the date
    wm.plot_label(ax_map,
                  '%04d-%02d-%02d:%02d' % (dte.year,dte.month,
                                           dte.day,dte.hour),
                  facecolor=fig.get_facecolor(),
                  x_fraction=0.02,
                  horizontalalignment='left')
    
    ax_scp=fig.add_axes([0.6,0.04,0.39,0.95])

    plot_scatter(ax_scp,field,dwr_obs,dte,pressure_range)

    # Join each station name to its location on the map
    # Need another axes, filling the whole fig
    ax_full=fig.add_axes([0,0,1,1])
    ax_full.patch.set_alpha(0.0)  # Transparent background

    # Map location of a station in ax_full coordinates
    def pos_left(dwr_obs,stations,idx):
        latlon=DWR.get_station_location(dwr_obs,stations[idx])
        rp=ax_map.projection.transform_points(ccrs.PlateCarree(),
                                  numpy.asarray(latlon['longitude']),
                                  numpy.asarray(latlon['latitude']))
        new_lon=rp[:,0]
        new_lat=rp[:,1]

        result={}
        result['x']=0.01+0.485*((new_lon-(scale*-1))/(scale*2))
        result['y']=0.01+0.98*((new_lat-(scale*aspect*-1))/
                                           (scale*2*aspect))
        return result

    # Label location of a station in ax_full coordinates
    def pos_right(dwr_obs,stations,idx):
        result={}
        result['x']=0.51
        result['y']=0.04+(0.95/len(stations))*(idx+0.5)
        return result

    for i in range(0,len(stations)):
        p_left=pos_left(dwr_obs,stations,i)
        p_right=pos_right(dwr_obs,stations,i)
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

