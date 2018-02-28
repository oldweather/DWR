`Spaghetti contours main page <spaghetti_contour.html>`_

Spaghetti contours: 20CR2c
==========================

.. raw:: html

    <center>
    <table><tr><td>
    <a href="https://github.com/oldweather/DWR/raw/master/analyses/spaghetti_contour/Spaghetti_prmsl_1903102218.png"><img src="https://github.com/oldweather/DWR/raw/master/analyses/spaghetti_contour/Spaghetti_prmsl_1903102218.png""></a></td></tr>
    <tr><td> MSLP Contours for 20CR2c for October 22nd, 1903 (at 6pm). Blue lines are contours from each of ensemble member, black lines the contours of the ensemble mean (only shown where the ensemble spread is less than 3hPa). Yellow dots are observations asssimilated.</td></tr>
    </table>
    </center>

Collect the data (prmsl ensemble and observations from 20CR2c for 1903):

.. code-block:: python

    import Meteorographica.data.twcr as twcr
    twcr.fetch_data_for_year('prmsl',1903,version='3.5.1')
    twcr.fetch_data_for_year('observations',1903,version='3.5.1')

Script to make the figure:

.. literalinclude:: ../../../analyses/spaghetti_contour/prmsl_20CR.py

