`Scatter-and-contour main page <scatter_and_contour.html>`_

Visualising uncertainty: 20CR2c spaghetti contours & DWR data video
===================================================================

.. raw:: html

    <center>
    <table><tr><td>
    <iframe src="https://player.vimeo.com/video/252493957?title=0&byline=0&portrait=0" width="730" height="411" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></td></tr>
    <tr><td>MSLP spaghetti-contour plot for 20CR2c (left), and comparison with DWR obs at the station locations (right) over October 1903.</td></tr>
    </table>
    </center>

Collect the reanalysis data (prmsl ensemble from 20CR2c for 1903):

.. code-block:: python

    import Meteorographica.data.twcr as twcr
    twcr.fetch_data_for_year('prmsl',1903,version='3.5.1')

Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../../../analyses/scatter+contour/video/scatter+contour.py

To make the video, it is necessary to run the script above about 3000 times - giving an image for every 15-minute period in a month. The best way to do this is system dependent - the script below does it on the Met Office SPICE cluster - it will need modification to run on any other system. (Could do this on a single PC, but it will take many hours).

.. literalinclude:: ../../../analyses/scatter+contour/video/make_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i scatter+contour/\*1903\*.png \
           -c:v libx264 -threads 16 -preset slow -tune animation \
           -profile:v high -level 4.2 -pix_fmt yuv420p -crf 25 \
           -c:a copy scatter+contour.mp4
