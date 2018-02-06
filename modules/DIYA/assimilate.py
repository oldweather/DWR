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
from sklearn.utils import check_random_state
import iris
import numpy
import copy

# Control the order of the vector dimensions of a cube, so the 
#  numpy array of data has the expected shape.
def cube_order_dimensions(cube,dims_list):
    crds2=cube.coords()
    crds=copy.deepcopy(crds2)
    # Keep only the vector dimensions
    for crdi in range(0,len(crds2)):
        if len(crds2[crdi].points)==1: crds.remove(crds2[crdi])
    if len(crds)!=len(dims_list):
        raise StandardError("Cube has %d vector dimensions and %d were specified" %
                             (len(crds),len(dims_list)))
    odr=range(0,len(dims_list))
    for dim_i in range(0,len(dims_list)):
        try:
            odr[dim_i]=[index for index in range(len(crds)) 
                      if crds[index].long_name==dims_list[dim_i]][0]
        except IndexError:
            raise StandardError("Cube does not have vector dimension %s" %
                                 dims_list[dim_i])
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
    if len(latitudes)>1:
        interpolated=cube_order_dimensions(interpolated,('member',
                                            'latitude','longitude'))
    # This interpolates at each lat,lon pair - we only want the ith lat and ith lon
    result=numpy.diagonal(interpolated.data,axis1=1,axis2=2).copy()
    return result

# Given a target cube, a constraints cube, and a set of 
#  observations, make a constrained cube.
def constrain_cube(target,constraints,obs,obs_error=0.1,random_state=None):
    X=build_X_matrix_from_cube(constraints,obs.latitude,
                                           obs.longitude)
    Y=cube_order_dimensions(target,('member','latitude','longitude'))
    # Make a different set of perturbed obs for each ensemble member
    perturbed_obs=numpy.zeros([X.shape[0],len(obs.latitude)])
    random_state = check_random_state(random_state)
    for member in range(0,X.shape[0]):
        perturbed_obs[member,:]=obs.value+random_state.normal(
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
                      random_state=random_state, 
                      selection='cyclic')
    for lat_i in range(0,Y.data.shape[1]):
        for lon_i in range(0,Y.data.shape[2]):
            y=Y[:,lat_i,lon_i].data
            Y.data[:,lat_i,lon_i]=constrain_point(y,X,model,perturbed_obs)
    return Y

# Constrain the ensemble at a selected point
def constrain_point(target,constraint,model,obs):
    fit=model.fit(constraint,target)
    residuals=target-fit.predict(constraint)
    predictions=fit.predict(obs)+residuals
    return predictions


