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
This module provides a python API to :doc:`the data recently digitised from the UK Daily Weather Reports <../../docs/DWR>`.

Access to the data is through the :func:`load_observations` function:

.. code-block:: python

    import DWR
    import datetime
    obs=DWR.load_observations('prmsl',
                              datetime.datetime(1903,10,1,0),
                              datetime.datetime(1903,10,31,23))

Will load the mslp observations (as a :obj:`pandas.DataFrame`) from the whole of October 1903.

Observations are typically made twice a day. It's often useful to estimate the observed value at other times of day. :func:`at_station_and_time` does this :

.. code-block:: python

    value=DWR.at_station_and_time(obs,'ABERDEEN',
                                  datetime.datetime(1903,10,12,13,30))

estimates the Aberdeen observation at 1:30pm on 12 October 1903 by linear interpolation between the nearest previous and subsequent observations. obs is the :obj:`pandas.DataFrame` loaded above.

It's nice to have easy access to station locations:

.. code-block:: python

   posn=DWR.get_station_location(obs,'ABERDEEN')

gets the position (posn['latitude'] and posn['longitude']) of the Aberdeen station. Note that these positions have low accuracy: the DWR has poor station metadata and we often don't know which station was in use at which time. This call returns the location of Aberdeen, rather than the location of the weather station in Aberdeen.

The station names are stored in ALLCAPS with no spaces; for pretty output we want correctly capitalised and spaced strings

.. code-block:: python

   DWR.pretty_name('FORTWILLIAM')

returns 'Fort William'.

|
"""


from .load import *
from .names import *

