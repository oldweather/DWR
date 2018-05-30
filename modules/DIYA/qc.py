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

# Replicate the 20CR2c observations quality control

import iris
import numpy
import pandas
import Meteorographica.data.twcr as twcr

def qc_plausible_range(obs,min=880.0,max=1060.0):
    """Checks the obs value for plausibility.

    Args:
        obs (:obj:`pandas.DataFrame`): Observations. Dataframe must have column 'value', and value should have same units as max and min.
        min (:obj:`float`): Minimum plausible value, defaults to 880.
        max (:obj:`float`): Maximum plausible value, defaults to 1060.

    Returns:
        (:obj:`pandas.Series`): True where obs['value' between min and max, False otherwise.

    |
    """

    plausible = (obs['value']>=min) & (obs['value']<=max)
    return plausible

def qc_compare_reanalysis(obs,variable='prmsl',version='2c'):
    """Get 20CR ensemble values at the time and place of each observation.

    Args:
        obs (:obj:`pandas.DataFrame`): Observations. Dataframe must have columns 'latitude, 'longitude, and 'dtm' - the last a datetime.datetime.
        variable (:obj:`str`): Which 20CR variable to compare to. Defaults to 'prmsl'
        version (:obj:`str`): Which 20CR version to load data from. Defaults to '2c'

    Returns
        :obj:`pandas.Series`): Reanalyis ensemble associated with each observation.

    |
    """

    old_idx=obs.index
    obs=obs.reset_index() # index values 0-n
    ob_times=obs['dtm'].unique()
    results=[None]*len(obs)
    for ob_time in ob_times:
        ot=pandas.to_datetime(ob_time)
        ensemble=twcr.load(variable,ot.year,ot.month,ot.day,
                                ot.hour+ot.minute/60.0,
                                                version=version)
        # Units hack - assumes obs in hPa (if prmsl)
        if variable=='prmsl': 
            ensemble.data=ensemble.data/100.0 # to hPa
        interpolator = iris.analysis.Linear().interpolator(ensemble, 
                                       ['latitude', 'longitude'])
        this_time=obs['dtm'][obs['dtm']==ob_time].index
        for ob_idx in this_time:
            ensemble=interpolator([obs.latitude[ob_idx],obs.longitude[ob_idx]])
            results[ob_idx]=ensemble.data

    return pandas.Series(results,index=old_idx)

def qc_first_guess(obs,nsd=3,osd=2,comparison=None,variable='prmsl',version='2c'):
    """Checks the obs value against the 20CR ensemble.

    Args:
        obs (:obj:`pandas.DataFrame`): Observations. Dataframe must have columns 'latitude, 'longitude, 'value', and 'dtm' - the last a datetime.datetime.
        nsd (:obj:`float`): Number of standard deviations for rejection threshold. Defaults to 3.
        osd (:obj:`float`): Observation standard deviation. Defaults to 2.
        comparison (:obj:`pandas.Series`): Reanalysis ensemble values at the time and place of each observation. Defaults to None - calculate them.
        variable (:obj:`str`): Which 20CR variable to compare to. Defaults to 'prmsl'
        version (:obj:`str`): Which 20CR version to load data from. Defaults to '2c'

    For each observation, loads the 20CR ensemble at the time of observation, extracts the mean and standard deviation at the time and place of observation, and compares ob-ensemble mean with the expected difference given the ensemble spread and observation error sqrt(ensemble sd**2 + osd**2). If the observed difference is greater than nsd times the expected difference, mark ob with false, otherwise with true.

    Returns:
        (:obj:`pandas.Series`): True where ob-ensemble mean within expected difference from 20CR spread, False otherwise.

    |
    """

    results=[None]*len(obs)

    if comparison==None:
        comparison=qc_compare_reanalysis(obs,variable=variable,version=version)

    for idx in range(len(obs)):
        ens_mean  = numpy.mean(comparison.values[idx])
        ens_sd    = numpy.std(comparison.values[idx],ddof=1)
        expected  = numpy.sqrt(osd**2+ens_sd**2)
        deviation = abs(obs.value.values[idx]-ens_mean)
        if (deviation/expected)<nsd:
            results[idx]=True
        else:
            results[idx]=False

    return pandas.Series(results,index=obs.index)
    
        

