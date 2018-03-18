How to replicate and extend this
================================

This document is organised and shared as a piece of software. It is a set of files (some code, some documentation) kept under version control in a `git repository <https://en.wikipedia.org/wiki/Git>`_. The repository is hosted on `github <https://github.com/>`_ (and the documentation made with `github pages <https://pages.github.com/>`_). The repository is `<https://github.com/oldweather/DWR>`_.

If you are familliar with github, you already know what to do; if not, ask a local software specialist for advice. In short, go to `the repository address <https://github.com/oldweather/DWR>`_ and hit the 'fork' button (top right) - this will make your own copy of the whole thing. Then 'clone or download' your fork to your PC, and you will have a full, local copy to work with.

To run the programs in your local copy, there are two more steps:

1. Install the `Meteorographica <https://philip-brohan.github.io/Meteorographica/>`_ python module (and all of its dependencies). This handles access to reanalysis data and provides plotting functions.
2. Add the 'modules' directory in the repository to python's search path. If your downloaded copy is in directory /home/whoever/DWR, then you need to add '/home/whoever/DWR/modules' to the 'PYTHONPATH' environment variable. (Don't move the modules elsewhere, they will lose contact with the data files.)

You should then be able to run all the software in the repository and reproduce the results.

If you fix a bug, or introduce a improvement that should be incoporated in the original repository, please send a `pull request <https://help.github.com/articles/about-pull-requests/>`_.

Otherwise just go on to modify and build on this as you see fit. Please do let us know, by `raising an issue <https://github.com/oldweather/DWR/issues/new>`_.
