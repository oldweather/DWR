`Spaghetti contours main page <analysis_spaghetti_contour.html>`_

Spaghetti contours: 20CRvCERA
=============================

.. raw:: html

    <center>
    <table><tr><td>
    <a href="https://github.com/oldweather/DWR/raw/master/analyses/spaghetti_contour/Compare_mslp_1903102218.png"><img src="https://github.com/oldweather/DWR/raw/master/analyses/spaghetti_contour/Compare_mslp_1903102218.png""></a></td></tr>
    <tr><td>MSLP Contours for 20CR2c (left), and CERA20C (right) for October 22nd, 1903 (at 6pm). Blue lines are contours from each of 10 ensemble members, black lines the contours of the ensemble mean (only shown where the ensemble spread is less than 3hPa). Yellow dots are observations asssimilated by 20CR, red dots are new observations now available from DWR (not assimilated in the reanalyses).</td></tr>
    </table>
    </center>

Collect the data (prmsl ensemble and observations from 20CR2c, prmsl ensemble for CERA20C):

.. code-block:: python

    import Meteorographica.data.twcr as twcr
    twcr.fetch_data_for_year('prmsl',1903,version='3.5.1')
    twcr.fetch_data_for_year('observations',1903,version='3.5.1')
    import Meteorographica.data.cera20c as cera20c
    cera20c.fetch_data_for_month('prmsl',1903,10)

Script to make the figure:

.. literalinclude:: ../analyses/spaghetti_contour/compare_contours.py

