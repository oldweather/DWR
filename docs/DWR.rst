`Raise issue or make comment? <https://github.com/oldweather/DWR/issues/new?label=DWR>`_

The Daily Weather Reports
=========================

.. pull-quote::

    "It has been desired that a great many observations should be compared throughout the British Islands (with their neighbouring coasts and seas), at certain remarkable periods, to obtain the means of deliniating or mapping the atmosphere at successive times; and thence to deduce the order of those changes of wind and weather which affect navigation and fisheries especially, besides agriculture, health, and all out-door occupations.

    Such maps or charts should show the various horizontal or other currents of wind (existing within such an area) at one time, to which all other corresponding times should be reduced by allowing for the *difference of longitude*.

    They should show the pressure and temperature of those currents - and other facts, such as the presence of clouds, rain, lightning &c., at their respective localities.

    A sequence of such maps, compiled for special periods when changes have been most marked, would enable meteorologists to trace atmospheric waves as well as currents, both in plan and section, and would throw much light on meteorology."

   --Robert Fitzroy - `The weather book, a Manual of Practical Meteorology <https://books.google.co.uk/books?redir_esc=y&output=text&id=J4GDgpKKXCkC>`_ (1863)

To meet this need, Fitzroy created the `Daily Weather Reports <https://www.metoffice.gov.uk/learning/library/archive-hidden-treasures/daily-weather-reports>`_ (DWR). Starting on 3rd September 1860, and running up to the present day, these contain synoptic observations from weather stations in and around the British Isles, sent to the Met Office by telegraph. The stations included, and frequency of observations, vary through the period of the reports, but typically they contain data from about 50 stations, reported twice or four times daily.

`Digital images of the entire DWR series <https://digital.nmla.metoffice.gov.uk/archive/sdb%3Acollection|86058de1-8d55-4bc5-8305-5698d0bd7e13/>`_ are available online courtesy of the `National Meteorological Library and Archive <https://www.metoffice.gov.uk/learning/library>`_.

From about 1957, the observations reported in the DWR `are included in Met Office and international databases <https://www.research.ed.ac.uk/portal/en/publications/recent-observed-changes-in-severe-storms-over-the-united-kingdom-and-iceland(4362d146-ef64-4b18-b5df-14378b25c4e5).html>`_. The first hundred years of records, however, are only available on paper, and so are inaccessible to science.

Two projects have transcribed some of the earlier DWR reports: `A study of severe storms across the British Isles <https://www.research.ed.ac.uk/portal/en/publications/fluctuations-in-autumnwinter-severe-storms-over-the-british-isles-1920-to-present(7135f643-9419-4e6a-b2e9-91bd137e13be).html>`_, transcribed a subset of the pressure observations over the period 1919-1960, and the citizen science project `weatherrescue.org <http://weatherrescue.org>`_ is making a more comprehensive transcription. 

The observations transcribed by those two projects are included in this repository.

.. toctree::
   :maxdepth: 2

   data/data_from_lisa_files 
   data/data_from_weatherrescue

An API for these observations is provided by a python module:

.. toctree::
   :maxdepth: 2

   modules/module_DWR.rst 
