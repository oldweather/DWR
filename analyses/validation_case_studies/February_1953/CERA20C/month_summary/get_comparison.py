# UK region weather plot 
# Collect reanalysis comparison data for
# Every DWR ob in a month

import os
import datetime
import pandas
import iris
import pickle

import Meteorographica.data.cera20c as cera20c

import DWR

# Set output file
opfile=("%s/images/DWR/vcs_cera20c_1953_month_comparison.pkl" % 
                os.getenv('SCRATCH'))

obs=DWR.load_observations('prmsl',
                          datetime.datetime(1953,2,1,6),
                          datetime.datetime(1953,2,28,18))
# Remove stations already in ISPD
obs=obs[~obs['name'].isin(['LERWICK','STORNOWAY','VALENTIA',
                           'CULDROSE','GORLESTON','LEUCHARS'])]

# Get a list of all the times where there is at least 1 observation.
ob_times=obs['dtm'].unique()
# At each such time, get the reanalysis ensemble at all the
#   stations reporting at that time.
ensembles=[]
observations=[]
for ob_time in ob_times:
    ob_time=pandas.to_datetime(ob_time)
    print ob_time
    prmsl=cera20c.load('prmsl',ob_time.year,ob_time.month,ob_time.day,
                            ob_time.hour+ob_time.minute/60.0)
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
        
