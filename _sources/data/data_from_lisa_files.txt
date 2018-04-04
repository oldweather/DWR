
Data from an earlier digitisation project
=========================================

As part of `a study of severe storms across the British Isles <https://www.research.ed.ac.uk/portal/en/publications/fluctuations-in-autumnwinter-severe-storms-over-the-british-isles-1920-to-present(7135f643-9419-4e6a-b2e9-91bd137e13be).html>`_, some observations from the Daily Weather Reports were (commercially) transcribed in the early 2000's. This transcription project covered the period 1919-1960, but only transcribed part of the observations: only pressure and pressure tendencies were transcribed, and only from stations in the British Isles reporting four times a day. Also, the 'late arrivals and corrections' section of the reports was not included.

The raw transcription output has not survived, but the transcriptions were processed into `station files <https://github.com/oldweather/DWR/tree/master/Lisa_storms/raw.data>`_ containing up to eight mean-sea-level-pressure observations a day (four observations and another four constructed from the 3-hour pressure tendencies).

.. literalinclude:: ../../Lisa_storms/raw.data/3hr_Aberdeen_1919-1956.dat
    :lines: 457-468

One complication with the DWR is that exact observation locations are not given, only approximate locations (e.g. 'Aberdeen'). For MSLP, observations exact locations are not vital, so `a nominal location <https://github.com/oldweather/DWR/blob/master/Lisa_storms/metadata/names.csv>`_ has been assigned for each station.

Another difficulty with the station files is that they don't give exact times for the observations (they weren't needed by the original study). The eight values in the station files for each day are the values on the DWR page for that day, and both the format of the page and the times of observations changed over the period 1919-1960.

To make the data easily useable, the station files have been conferted into the same monthly data format used for `weatherrescue.org data <data_from_weatherrescue.html>`_; assigning latitudes, longitudes, and times in the process.

.. literalinclude:: ../../Lisa_storms/scripts/to_DWR_format.py

Both the `original station files <https://github.com/oldweather/DWR/tree/master/Lisa_storms/raw.data>`_ and the `final monthly files <https://github.com/oldweather/DWR/tree/master/data_from_Lisa>`_ are included in this repository. An API for the final monthly data is provided by `a python module <../modules/module_DWR.html>`_.
