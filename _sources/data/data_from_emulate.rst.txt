Data from EMULATE
=================

As part of the work to make the `EMULATE mean-sea-level pressure dataset <https://www.metoffice.gov.uk/hadobs/emslp/>`_, some observations from the Daily Weather Reports were (commercially) transcribed in the early 2000's. This transcription project covered the period 1856-1881, but only transcribed part of the observations: only pressure and pressure tendencies were transcribed, and only from selected stations. These data were not actually used in EMULATE, and this is the first time they have been released.

The transcriptions were collected into `spreadsheet files <https://github.com/oldweather/DWR/tree/master/Emulate>`_:

.. literalinclude:: ../../Emulate/original_data_csv/DWR_stations.Aberdeen.csv
    :lines: 1-36

One complication with the DWR is that exact observation locations are not given, only approximate locations (e.g. 'Aberdeen'). For MSLP, observations exact locations are not vital, so `a nominal location <https://github.com/oldweather/DWR/blob/master/Lisa_storms/metadata/names.csv>`_ has been assigned for each station.

To make the data easily useable, the station files have been converted into the same monthly data format used for `weatherrescue.org data <data_from_weatherrescue.html>`_; assigning latitudes, longitudes, and times in the process.

.. literalinclude:: ../../Emulate/scripts/to_DWR_format.py

