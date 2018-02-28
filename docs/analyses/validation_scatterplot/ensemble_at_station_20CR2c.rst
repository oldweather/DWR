`Ensemble comparison main page <ensemble_at_station.html>`_

Compare DWR and 20CR2c reanalysis ensemble at station locations
===============================================================

.. raw:: html

    <center>
    <table><tr><td>
    <a href="https://github.com/oldweather/DWR/raw/master/analyses/validation_scatterplot/DWR_v_20CR_1901012218.png"><img src="https://github.com/oldweather/DWR/raw/master/analyses/validation_scatterplot/DWR_v_20CR_1901012218.png"></a></td></tr>
    <tr><td>MSLP as observed at each DWR station (red line), as reconstructed by the 20CR2c ensemble at the station location (blue dots) for January 22nd, 1901 (at 6pm).</td></tr>
    </table>
    </center>

Collect the data (prmsl ensemble from 20CR2c for 1901):

.. code-block:: python

    import Meteorographica.data.twcr as twcr
    twcr.fetch_data_for_year('prmsl',1901,version='3.5.1')

Script to make the figure:

.. literalinclude:: ../../../analyses/validation_scatterplot/validation_scatterplot.py
