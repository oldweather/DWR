# UK region weather plot 
# Collect reanalysis comparison data for
# Every DWR ob in a month

import os
import datetime
import pandas
import iris
import pickle

import Meteorographica.data.twcr as twcr

import DWR

# Set output file
opfile=("%s/images/DWR/vcs_cera20c_1903_month_comparison.pkl" % 
                os.getenv('SCRATCH'))

obs=DWR.load_observations('prmsl',
                          datetime.datetime(1903,10,1,6),
                          datetime.datetime(1903,10,31,18))
# Remove stations already in ISPD
obs=obs[~obs['name'].isin(['BODO','HAPARANDA','HERNOSAND',
                           'STOCKHOLM','WISBY','ABERDEEN',
                           'VALENCIA','FANO','SCILLY','JERSEY',
                           'LISBON','DUNGENESS','THEHELDER',
                           'BERLIN'])]

# Get a list of all the times where there is at least 1 observation.
ob_times=obs['dtm'].unique()
# At each such time, get the reanalysis ensemble at all the
#   stations reporting at that time.
ensembles=[]
observations=[]
for ob_time in ob_times:
    ob_time=pandas.to_datetime(ob_time)
    print ob_time
    prmsl=twcr.load('prmsl',ob_time.year,ob_time.month,ob_time.day,
                            ob_time.hour+ob_time.minute/60.0,
                                                       version='2c')
    prmsl.data=prmsl.data/100.0 # to hPa
    interpolator = iris.analysis.Linear().interpolator(prmsl, 
                                   ['latitude', 'longitude'])
    obs_current=obs[obs['dtm']==ob_time]
    for ob in obs_current.itertuples():
        ensemble=interpolator([ob.latitude,ob.longitude])
        ensembles.append([ensemble.data])
        observations.append(ob.value)

afile = open(opfile, 'wb')
pickle.dump({'ensembles': ensembles,
             'observations':observations}, afile)
afile.close()
        
