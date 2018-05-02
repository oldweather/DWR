Validating 20CR3 against DWR data: October 1903 station scatterplot
====================================================================

.. seealso:: 
    * :doc:`Video version <reliability_and_error_video>`
    * :doc:`Scatter plot <scatter_and_contour>`
    * :doc:`Same diagnostic but for 20CR version 2c <../20CR2c/reliability_and_error>`
    * :doc:`Same diagnostic but for CERA20C <../CERA20C/reliability_and_error>`
    * :doc:`Same diagnostic but for February 1953 <../../February_1953/20CR2c/reliability_and_error>`

.. figure:: ../../../../../analyses/validation_case_studies/October_1903/20CRv3/scatter+contour/Scatter+contour_1903102518.png
   :width: 650px
   :align: center
   :figwidth: 700px

   On the left: MSLP Contours for 20CR v3, observations assimilated (yellow circles), DWR observations not assimilated (larger circles, coloured by deviation from reanalysis: blue - observation lower, red - observation higher).

   On the right: MSLP observation (red line), and ensemble values (blue dots) at the location of each DWR station.

|

Collect the reanalysis data (observations and prmsl ensemble from 20CR3 for October 1903):

.. note:: 20CRv3 has not yet been released, so the data retrieval script will currently work only for a privileged few.

.. literalinclude:: ../../../../../analyses/validation_case_studies/October_1903/20CRv3/get_data.py

Script to make the figure:

.. literalinclude:: ../../../../../analyses/validation_case_studies/October_1903/20CRv3/scatter+contour/scatter+contour.py

