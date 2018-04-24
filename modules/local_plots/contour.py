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

# Plot reanalysis pressure and DWR observations

import iris
import iris.analysis
import DWR
import matplotlib
import matplotlib.cm
import cartopy.crs as ccrs
import numpy
import Meteorographica.weathermap as wm
import collections

def plot_contour(ax,extent,dte,field,obs_r,dwr_obs,
             projection=ccrs.RotatedPole(pole_longitude=177.5,
                                         pole_latitude=35.5),
             obs_radius=0.15,
             contour_levels=numpy.arange(870,1050,10),
             contour_width=0.1,
             contour_mask=3,
             n_contours=None,
             dwr_color='anomaly',
             dwr_anomaly_range=20.0,
             dwr_radius=0.25):
    """Make a mslp contour plot with DWR observations

    Args:
        ax (:`cartopy.axes`): Axes to hold the plot
        extent (:obj:`list`) Plot extent (lon.min,lon.max,lat.min,lat.max)
        dte (:obj:`datetime.datetime`): Time of plot
        field (:obj:`iris.Cube.cube`): Reanalysis mslp ensemble
        obs_r (:obj:`pandas.DataFrame`): Reanalysis observations.
        dwr_obs (:obj:`pandas.DataFrame`): DWR observations.

    |
    """

    ax.set_axis_off()
    ax.set_extent(extent, crs=projection)
    ax.background_patch.set_facecolor((0.88,0.88,0.88,1))
    wm.add_grid(ax)
    land_img=ax.background_img(name='GreyT', resolution='low')

    # Plot the 20CR obs
    if obs_r is not None:
        if 'Assimilation.indicator' in obs_r.index: # in V2 only
            obs_s=obs_r.loc[(obs_r['Assimilation.indicator']==1)]
            if not obs_s.empty:
                wm.plot_obs(ax,obs_s,radius=obs_radius)
            obs_s=obs_r.loc[(obs_r['Assimilation.indicator']==0)]
            if not obs_s.empty:
                wm.plot_obs(ax,obs_s,radius=obs_radius,
                            facecolor='grey',edgecolor='yellow',
                                             zorder=2.4)
        else:
            if not obs_r.empty:
                wm.plot_obs(ax,obs_r,radius=obs_radius)
        

    # Plot the DWR obs
    if dwr_obs is not None:
        stations=collections.OrderedDict.fromkeys(
                         dwr_obs.loc[:,'name']).keys()
        if dwr_color=='anomaly':
            cmap = matplotlib.cm.get_cmap('coolwarm')
            interpolator = iris.analysis.Linear().interpolator(field, 
                                       ['latitude', 'longitude'])
            interpolated={}
            for station in stations:
                try:
                    interpolated[station]=DWR.at_station_and_time(
                                                      dwr_obs,station,dte)
                except StandardError:
                    interpolated[station]=None
                latlon=DWR.get_station_location(dwr_obs,station)
                ensemble=interpolator([latlon['latitude'],
                                       latlon['longitude']])
                if interpolated[station] is None:
                    wm.plot_obs(ax,dwr_obs[dwr_obs['name']==station],
                         lat_label='latitude',lon_label='longitude',
                         radius=dwr_radius,
                         facecolor='grey',edgecolor='black')
                else:
                    stn_diff=interpolated[station]-numpy.mean(ensemble.data)
                    dfn=max(0.01,min(0.99,stn_diff/dwr_anomaly_range+0.5))
                    stn_color=cmap(dfn)
                    wm.plot_obs(ax,dwr_obs[dwr_obs['name']==station],
                         lat_label='latitude',lon_label='longitude',
                         radius=dwr_radius,
                         facecolor=stn_color,edgecolor='black')
        else:
            for station in stations:
                wm.plot_obs(ax,dwr_obs[dwr_obs['name']==station],
                     lat_label='latitude',lon_label='longitude',
                     radius=dwr_radius,
                     facecolor=dwr_color,edgecolor='black')
        
    # For each ensemble member, make a contour plot
    for m in field.coord('member').points:
        if n_contours is not None:
            if m>n_contours: break
        prmsl_e=field.extract(iris.Constraint(member=m))
        CS=wm.plot_contour(ax,prmsl_e,
                       levels=contour_levels,
                       colors='blue',
                       label=False,
                       linewidths=contour_width,
                       zorder=30)
    # Add the ensemble mean - with labels
    prmsl_m=field.collapsed('member', iris.analysis.MEAN)
    CS=wm.plot_contour(ax,prmsl_m,
                       levels=contour_levels,
                       colors='grey',
                       label=False,
                       linewidths=1,
                       zorder=1)
    # Mask out mean where uncertainties large
    prmsl_s=field.collapsed('member', iris.analysis.STD_DEV)
    prmsl_m.data[numpy.where(prmsl_s.data>contour_mask)]=numpy.nan
    CS=wm.plot_contour(ax,prmsl_m,
                       levels=contour_levels,
                       colors='black',
                       label=True,
                       linewidths=2,
                       zorder=50)
