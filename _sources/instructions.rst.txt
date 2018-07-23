How to use this dataset
=======================

This dataset is kept under version control in a `git repository <https://en.wikipedia.org/wiki/Git>`_. The repository is hosted on `GitHub <https://github.com/>`_ (and the documentation made with `GitHub Pages <https://pages.github.com/>`_). The repository is `<https://github.com/oldweather/DWR>`_.

If you are familiar with GitHub, you already know `what to do <https://github.com/oldweather/DWR>`_: If you'd prefer not to bother with that, you can download the whole dataset as `a zip file <https://github.com/oldweather/DWR/archive/master.zip>`_.

The data themselves are distibuted as :doc:`a set of plain text files <view_by_month/months>` (in the 'data' directory - note that the repository also contains the source data files from which they were constructed). Also included is :doc:`a python module providing an API to the data <modules/module_DWR>` - to use this module, download the dataset and then install it with:

.. code-block:: sh

   python setup.py install --user

You should then be able to run scripts like:

.. code-block:: python

   import DWR
   import datetime
   obs=DWR.load_observations('prmsl',
                             datetime.datetime(1903,10,1,12),
                             datetime.datetime(1903,10,2,12))

If you use this dataset, please let us know, by `raising an issue <https://github.com/oldweather/DWR/issues/new>`_. You are not obliged to do this, but it would help the campaign to rescue even more data.

