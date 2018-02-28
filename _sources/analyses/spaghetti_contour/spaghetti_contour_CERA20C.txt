`Spaghetti contours main page <spaghetti_contour.html>`_

Spaghetti contours: CERA20C
===========================

.. raw:: html

    <center>
    <table><tr><td>
    <a href="https://github.com/oldweather/DWR/raw/master/analyses/spaghetti_contour/Spaghetti_prmsl_1903102218_cera.png"><img src="https://github.com/oldweather/DWR/raw/master/analyses/spaghetti_contour/Spaghetti_prmsl_1903102218_cera.png""></a></td></tr>
    <tr><td> MSLP Contours for CERA20C for October 22nd, 1903 (at 6pm). Blue lines are contours from each of ensemble member, black lines the contours of the ensemble mean (only shown where the ensemble spread is less than 3hPa).</td></tr>
    </table>
    </center>

Collect the data (prmsl ensemble from CERA20C for October 1903):

.. code-block:: python

    import Meteorographica.data.cera20c as cera20c
    cera20c.fetch_data_for_month('prmsl',1903,10)

Script to make the figure:

.. literalinclude:: ../../../analyses/spaghetti_contour/prmsl_CERA.py

