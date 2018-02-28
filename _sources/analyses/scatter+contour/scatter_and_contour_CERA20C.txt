`Scatter-and-contour main page <scatter_and_contour.html>`_

Visualising uncertainty: CERA20C spaghetti contours & DWR data
==============================================================

.. raw:: html

    <center>
    <table><tr><td>
    <a href="https://github.com/oldweather/DWR/raw/master/analyses/scatter%2Bcontour/Scatter%2Bcontour_1901012218.cera20c.png"><img src="https://github.com/oldweather/DWR/raw/master/analyses/scatter%2Bcontour/Scatter%2Bcontour_1901012218.cera20c.png"></a></td></tr>
    <tr><td>MSLP spaghetti-contour plot for 20CR2c (left), and comparison with DWR obs at the station locations (right) for January 22nd, 1901 (at 6pm).</td></tr>
    </table>
    </center>

Collect the reanalysis data (prmsl ensemble from CERA20C for January 1901):

.. code-block:: python

    import Meteorographica.data.cera20c as cera20c
    cera20c.fetch_data_for_year('prmsl',1901,1)

Script to make the figure:

.. literalinclude:: ../../../analyses/scatter+contour/scatter+contour.cera20c.py

