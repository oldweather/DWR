`Ensemble_comparison main page <analysis_ensemble_at_station.html>`_

Compare DWR and CERA20C reanalysis ensemble at station locations
================================================================

.. raw:: html

    <center>
    <table><tr><td>
    <a href="https://github.com/oldweather/DWR/raw/master/analyses/validation_scatterplot/DWR_v_CERA_1901012218.png"><img src="https://github.com/oldweather/DWR/raw/master/analyses/validation_scatterplot/DWR_v_CERA_1901012218.png"></a></td></tr>
    <tr><td>MSLP as observed at each DWR station (red line), as reconstructed by the CERA20C ensemble at the station location (blue dots) for January 22nd, 1901 (at 6pm).</td></tr>
    </table>
    </center>

Collect the data (prmsl ensemble from CERA20C):

.. code-block:: python

    import Meteorographica.data.cera20c as cera20c
    cera20c.fetch_data_for_month('prmsl',1901,1)

Script to make the figure:

.. literalinclude:: ../analyses/validation_scatterplot/validation_scatterplot.cera20c.py
