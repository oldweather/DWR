
Compare DWR and reanalysis obs. coverage
========================================

.. raw:: html

    <center>
    <a href="https://github.com/oldweather/DWR/raw/master/analyses/compare_coverage/Coverage.png"><img src="https://github.com/oldweather/DWR/raw/master/analyses/compare_coverage/Coverage.png" width="740"></a>
    <p>Obs coverage in 20CR2c (left), and in DWR (right)</p>
    </center>

Collect the data (observations from 20CR2c):

.. code-block:: python

    import Meteorographica.data.twcr as twcr
    twcr.fetch_data_for_year('observations',1901,version='3.5.1')

Script to make the figure:

.. literalinclude:: ../analyses/compare_coverage/Jan_1901_sbs.py
