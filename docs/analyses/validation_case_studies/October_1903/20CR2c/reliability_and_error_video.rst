Validating 20CR2c against DWR data: October 1903 station error video
====================================================================

.. seealso:: 
    * :doc:`Static version <reliability_and_error>`
    * :doc:`Scatter plot <scatter_and_contour_video>`
    * :doc:`Same diagnostic but for 20CR version 3 <../20CR3/reliability_and_error_video>`
    * :doc:`Same diagnostic but for CERA20C <../CERA20C/reliability_and_error_video>`
    * :doc:`Same diagnostic but for February 1953 <../../February_1953/20CR2c/reliability_and_error_video>`

.. raw:: html

    <center>
    <table><tr><td><center>
    <iframe src="https://player.vimeo.com/video/267250802?title=0&byline=0&portrait=0" width="795" height="448" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></center></td></tr>
    <tr><td><center>On the left: MSLP Contours for 20CR v2c, observations assimilated (yellow circles), DWR observations not assimilated (larger circles, coloured by deviation from reanalysis: blue - observation lower, red - observation higher). <p>Top right: Scatter plot of ensemble-observation against observation at each DWR station. <p>Bottom right: Scatter plot of ensemble standard deviation against ensemble-mean - observation.</center></td></tr>
    </table>
    </center>

|

Collect the reanalysis data (observations and prmsl ensemble from 20CR2c for 1903):

.. literalinclude:: ../../../../../analyses/validation_case_studies/October_1903/20CRv2c/get_data.py

Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../../../../analyses/validation_case_studies/October_1903/20CRv2c/reliability+error/video/reliability+error.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i reliability+error/\*.png \
           -c:v libx264 -threads 16 -preset slow -tune animation \
           -profile:v high -level 4.2 -pix_fmt yuv420p -crf 25 \
           -c:a copy reliability+error.mp4

