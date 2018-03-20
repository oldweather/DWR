Meteorological Data Assimilation for Data Scientists
====================================================

Suppose we have an uncertain estimate of the weather (MSLP) at some point in the past, perhaps `from a reanalysis <reanalysis_and_uncertainty.html>`_, and then we get some new information, in the form of a station observation from that date and time. How can we use that new station observation to improve the MSLP estimate?

|

.. figure:: ../DA_exposition/one_station/With_FW_1903102218.png
   :width: 650px
   :align: center
   :figwidth: 700px

   MSLP Contours for 20CR2c for October 22nd, 1903 (at 6pm).

   `Spaghetti-contour plot <analyses/spaghetti_contour/spaghetti_contour.html>`_ of mean-sea-level pressure, and the location of the Fort William station (red dot), where we have new observational data from `Weather Rescue <http://weatherrescue.org>`_

|

We can edit the reanalysis ensemble at the location of the new observation - setting all ensemble members to the observed value, but we would like to do more than this, to use information from the observation at nearby locations as well. To decide how to modify the mslp at, say, Stornoway and London, in response to an observation at Fort William, we need to know mslp variability in those places relates to weather variability at the location of the observation. However, we can estimate this directly from the ensemble:

|

.. figure:: ../DA_exposition/place_to_place/lr+contour_1903102218.png
   :width: 650px
   :align: center
   :figwidth: 700px

   MSLP at Fort William, Stornoway, and London (October 22nd, 1903 at 6pm).

   The red dot marks Fort William, the blue Stornoway, and the black London. Scatter plots show relationship between their mslp, in the 20CR2c ensemble for this particular point in time.

|

In the 20CR2c ensemble, at this point in time, the mslp at Stornoway is highly correlated with that at Fort William, so an observation at Fort William is telling us a lot about the mslp at Stornoway, and we should move the mslp estimates at Stornoway in response to the observation in much the same way as we move the estimates at Fort William. At London, on the other hand, the mslp is almost uncorrelated with that at Fort William, so an observation at Fort William is telling us little about the mslp at London, and we should leave the ensemble at London unchanged whatever the observation at Fort William is.

We can formalise this by fitting a model (:obj:`sklearn.linear_model.LinearRegression`):

|

.. figure:: ../DA_exposition/place_to_place/before+after_1903102218.png
   :width: 650px
   :align: center
   :figwidth: 700px

   MSLP at Stornoway, before and after assimilating the Fort William observation.

   Scatter plots of 20CR2c ensemble pressures at Stornoway at 6pm on 22nd October 1903 against Fort William ensemble pressures. The Stornoway pressures are adjusted by fitting a linear regression (left plot) and then removing the fit from each value (right plot). We can do the same for the London pressures, but in that case the adjustment will make almost no difference, as the fit line has close to zero slope.

|

To assimilate the Fort William observation, we apply the same process illustrated above for Stornoway to each grid-point in the reanalyis field:

