
New observations from weatherescue.org
=======================================

The citizen science project `Weather Rescue <http:www.weatherrescue.org>`_ originally set out to transcribe observations from Fort Willan and Ben Nevis (in Scotland), and is now transcribing the DWR data for the beginning of the 20th century (1900-1910).

Weather rescue is providing the data as `monthly files <https://github.com/oldweather/DWR/tree/master/data_from_Ed>`_ for each variable - each line gives the `UTC <https://en.wikipedia.org/wiki/Coordinated_Universal_Time>`_ date and time (year, month, day, hour, minute), observation location (latitude and longitude), observation value (here mean-sea-level pressure in hPa) and station name:

.. literalinclude:: ../../data_from_Ed/1901/01/prmsl.txt
    :lines: 12-25

The `monthly files <https://github.com/oldweather/DWR/tree/master/data_from_Ed>`_ are included in this repository. An API for the final monthly data is provided by `a python module <../modules/module_DWR.html>`_.
