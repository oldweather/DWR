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

def plot_contour(ax,extent,dte,field,obs_r,dwr_obs,**kwargs):
    """Make a mslp contour plot with DWR observations

    Args:
        ax (:`cartopy.axes`): Axes to hold the plot
        extent (:obj:`list`) Plot extent (lon.min,lon.max,lat.min,lat.max)
        dte (:obj:`datetime.datetime`): Time of plot
        field (:obj:`iris.Cube.cube`): Reanalysis mslp ensemble
        obs_r (:obj:`pandas.DataFrame`): Reanalysis observations.
        dwr_obs (:obj:`pandas.DataFrame`): DWR observations.

    Kwargs:
        projection (:obj:`cartopy.crs`): Map projection to use, default UKV.
        obs_radius (:obj:`float`): Reanalysis obs plot size, default 0.15.
        contour_levels (:obj:`list`): Values to plot contours at, default numpy.arange(870,1050,10).
        contour_width (:obj:`float`): Width of member contour lines, default 0.1.
        contour_mask (:obj:`float`): Plot mean contours where spread < this, default 3.
        n_contours (:obj:`int`): Max. number of member contour to plot, default None - all members.
        dwr_color (:obj:`str`): Either a color name, or the string 'anomaly' (default) to color by pressure anomaly.
        dwr_anomaly_range (:obj:`float`): Anomaly color scale factor, default 20.
        dwr_radius (:obj:`float`): DWR obs plot size, default 0.25.

    |
    """

    # Set keyword argument defaults
    kwargs.setdefault('projection',ccrs.RotatedPole(pole_longitude=177.5,
                                                     pole_latitude=35.5))
    kwargs.setdefault('obs_radius',0.15)
    kwargs.setdefault('contour_levels',numpy.arange(870,1050,10))
    kwargs.setdefault('contour_width',0.1)
    kwargs.setdefault('contour_mask',3.0)
    kwargs.setdefault('n_contours',None)
    kwargs.setdefault('dwr_color','anomaly')
    kwargs.setdefault('dwr_anomaly_range',20.0)
    kwargs.setdefault('dwr_radius',0.25)

    ax.set_axis_off()
    ax.set_extent(extent,crs=kwargs.get('projection'))
    ax.background_patch.set_facecolor(ax.get_figure().get_facecolor())
    wm.add_grid(ax)
    land_img=ax.background_img(name='GreyT', resolution='low')

    # Plot the 20CR obs
    if obs_r is not None:
        if 'Assimilation.indicator' in obs_r.index: # in V2 only
            obs_s=obs_r.loc[(obs_r['Assimilation.indicator']==1)]
            if not obs_s.empty:
                wm.plot_obs(ax,obs_s,radius=kwargs.get('obs_radius'))
            obs_s=obs_r.loc[(obs_r['Assimilation.indicator']==0)]
            if not obs_s.empty:
                wm.plot_obs(ax,obs_s,radius=kwargs.get('obs_radius'),
                            facecolor='grey',edgecolor='yellow',
                                             zorder=2.4)
        else:
            if not obs_r.empty:
                wm.plot_obs(ax,obs_r,radius=kwargs.get('obs_radius'))
        

    # Plot the DWR obs
    if dwr_obs is not None:
        stations=collections.OrderedDict.fromkeys(
                         dwr_obs.loc[:,'name']).keys()
        if kwargs.get('dwr_color')=='anomaly':
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
                         radius=kwargs.get('dwr_radius'),
                         facecolor='grey',edgecolor='black')
                else:
                    stn_diff=interpolated[station]-numpy.mean(ensemble.data)
                    dfn=max(0.01,min(0.99,
                       stn_diff/kwargs.get('dwr_anomaly_range')+0.5))
                    stn_color=cmap(dfn)
                    wm.plot_obs(ax,dwr_obs[dwr_obs['name']==station],
                         lat_label='latitude',lon_label='longitude',
                         radius=kwargs.get('dwr_radius'),
                         facecolor=stn_color,edgecolor='black')
        else:
            for station in stations:
                wm.plot_obs(ax,dwr_obs[dwr_obs['name']==station],
                     lat_label='latitude',lon_label='longitude',
                     radius=kwargs.get('dwr_radius'),
                     facecolor=kwargs.get('dwr_color'),edgecolor='black')
        
    # For each ensemble member, make a contour plot
    for m in field.coord('member').points:
        if kwargs.get('n_contours') is not None:
            if m>kwargs.get('n_contours'): break
        prmsl_e=field.extract(iris.Constraint(member=m))
        CS=wm.plot_contour(ax,prmsl_e,
                       levels=kwargs.get('contour_levels'),
                       colors='blue',
                       label=False,
                       linewidths=kwargs.get('contour_width'),
                       zorder=30)
    # Add the ensemble mean - with labels
    prmsl_m=field.collapsed('member', iris.analysis.MEAN)
    CS=wm.plot_contour(ax,prmsl_m,
                       levels=kwargs.get('contour_levels'),
                       colors='grey',
                       label=False,
                       linewidths=1,
                       zorder=1)
    # Mask out mean where uncertainties large
    prmsl_s=field.collapsed('member', iris.analysis.STD_DEV)
    prmsl_m.data[numpy.where(prmsl_s.data>kwargs.get('contour_mask'))]=numpy.nan
    CS=wm.plot_contour(ax,prmsl_m,
                       levels=kwargs.get('contour_levels'),
                       colors='black',
                       label=True,
                       linewidths=2,
                       zorder=50)
