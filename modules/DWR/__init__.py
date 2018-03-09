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
This package provides access to UK-region station observations recently digitised from the `Daily Weather Reports <https://www.metoffice.gov.uk/learning/library/archive-hidden-treasures/daily-weather-reports>`_

The data included come from two sources:

* The `Weather Rescue <http://weatherrescue.org>`_ citizen science project run by Ed Hawkins.
* A commercial digitisation project run back in 2002 by Lisa Alexander and Rob Allan, but never published.

The DWR provides synoptic observations, from around 50 stations in and around the UK, typically twice a day, but the list of stations providing observations, and the frequency of observation, both vary over the many years of the series.

The DWR provides observations of several variables, but so far we have digitised data only from one:

* Mean-sea-level pressure: 'mslp'

Access to the data is through the :func:`load_observations` function:

.. code-block:: python

    import DWR
    import datetime
    obs=DWR.load_observations('prmsl',
                              datetime.datetime(1903,10,1,0),
                              datetime.datetime(1903,10,31,23))

Will load the mslp observations (as a :obj:`pandas.DataFrame`) from the whole of October 1903.

|
"""


from load import *
from names import *

