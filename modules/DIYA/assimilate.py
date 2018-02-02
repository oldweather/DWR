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
"""
Functions to do EnKF-type data assimilation
"""

from sklearn.linear_model import ElasticNet
import iris
import numpy

# reduce a cube to a numpy array of its data with members
#  as its first dimension, and lat:lon points as
#  its second
def mll_order(cube):
    crds=cube.coords(dim_coords=True)
    if len(crds)!=3:
        raise StandardError("Cube has too many dimensions")
    odr=(0,1,2)
    try:
        odr=([index for index in range(len(crds)) 
                  if crds[index].long_name=='member'][0],
             [index for index in range(len(crds)) 
                  if crds[index].long_name=='latitude'][0],
             [index for index in range(len(crds)) 
                  if crds[index].long_name=='longitude'][0])
    except IndexError:
        raise StandardError("Cube does not have dimensions 'member'"+
                               "'latitude', and 'longitude'")
    result=cube.copy()
    result.transpose(new_order=odr)
    return result

# X-matrix for the model is a numpy array of dimension
#  (n.ensemble.members,n.stations)
# With the pressures at each station location
# Use this same matrix to fir each gridpoint
def build_X_matrix_from_cube(cube,latitudes,longitudes):
    locations = [('longitude', numpy.array(longitudes)),
                 ('latitude',  numpy.array(latitudes))]
    interpolated=cube.interpolate(locations,iris.analysis.Linear())
    interpolated=mll_order(interpolated)
    # Just want the numpy data
    result=interpolated.data
    # Flatten the lat and lon dimensions into a single one
    result=numpy.reshape(result,(result.shape[0],
                                 result.shape[1]*result.shape[2]))
    return result


# Given a target cube, a constraints cube, and a set of 
#  observations, make a constrained cube.
def constrain_cube(target,constraints,obs,obs_error=0):
    X=build_X_matrix_from_cube(constraints,obs.latitude,
                                           obs.longitude)
    Y=mll_order(target)
    # Make a different set of perturbed obs for each ensemble member
    perturbed_obs=numpy.zero([X.shape[0],len(obs.latitude)])
    for member in range(0,X.shape[0]):
        perturbed_obs[member,:]=obs.values+numpy.random.normal(
                                   loc=0,scale=obs_error,
                                   size=perturbed_obs.shape[1])
    # Use the same model at each grid point
    model=ElasticNet(alpha=1.0, l1_ratio=0.5,
                      fit_intercept=True,
                      normalize=False, 
                      precompute=False,
                      max_iter=1000, 
                      copy_X=False, 
                      tol=0.0001, 
                      warm_start=False, 
                      positive=False, 
                      random_state=None, 
                      selection='cyclic')
    for lat_i in range(0,Y.data.shape[1]):
        for lon_i in range(0,Y.data.shape[2]):
            y=Y[:,lat_i,lon_i]
            Y[:,lat_i,lon_i]=constrain_point(y,X,model,perturbed_obs)
    return Y

# Constrain the ensemble at a selected point
def constrain_point(target,constraint,model,obs):
    fit=model.fit(constraint,target)
    residuals=target-fit.predict(constraint)
    predictions=fit.predict(obs)+residuals
    return predictions


