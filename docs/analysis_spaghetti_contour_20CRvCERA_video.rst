`Spaghetti contours main page <analysis_spaghetti_contour.html>`_

Spaghetti contours: 20CRvCERA video
===================================

.. raw:: html

    <center>
    <table><tr><td>
    <iframe src="https://player.vimeo.com/video/252138404?title=0&byline=0&portrait=0" width="730" height="404" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></td></tr>
    <tr><td>MSLP Contours for 20CR2c (left), and CERA20C (right) for October 22nd, 1903 (at 6pm). Blue lines are contours from each of 10 ensemble members, black lines the contours of the ensemble mean (only shown where the ensemble spread is less than 3hPa). Yellow dots are observations asssimilated by 20CR, red dots are new observations now available from DWR (not assimilated in the reanalyses).</td></tr>
    </table>
    </center>

This is basically the same as `the single plot comparison <analysis_spaghetti_contour_20CRvCERA.html>`_. Only one such plot is made for every 15 minute period throughout October 1903, and they are then stitched together into a video.

Collect the data (prmsl ensemble and observations from 20CR2c, prmsl ensemble for CERA20C):

.. code-block:: python

    import Meteorographica.data.twcr as twcr
    twcr.fetch_data_for_year('prmsl',1903,version='3.5.1')
    twcr.fetch_data_for_year('observations',1903,version='3.5.1')
    import Meteorographica.data.cera20c as cera20c
    cera20c.fetch_data_for_month('prmsl',1903,10)

Script to make an individual frame - takes year, month, day, and hour as command-line options:

.. literalinclude:: ../analyses/spaghetti_contour/video/compare_contours.py

To make the video, it is necessary to run the script above about 3000 times - giving an image for every 15-minute period in a month. The best waty to do this is system dependent - the script below does it on the Met Office SPICE cluster - it will need modification to run on any other system. (Could do this on a single PC, but it will take many hours).

.. literalinclude:: ../analyses/spaghetti_contour/video/make_frames.py

To turn the thousands of images into a movie, use `ffmpeg <http://www.ffmpeg.org>`_

.. code-block:: shell

    ffmpeg -r 24 -pattern_type glob -i compare_contours/\*1903\*.png \
           -c:v libx264 -threads 16 -preset slow -tune animation \
           -profile:v high -level 4.2 -pix_fmt yuv420p -crf 25 \
           -c:a copy compare_contours.mp4
