========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |travis| |appveyor|
        | |codecov|
    * - package
      - | |commits-since|

.. |travis| image:: https://api.travis-ci.org/iotanbo/cpplibhub.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/iotanbo/cpplibhub

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/iotanbo/cpplibhub?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/iotanbo/cpplibhub

.. |codecov| image:: https://codecov.io/github/iotanbo/cpplibhub/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/iotanbo/cpplibhub

.. |commits-since| image:: https://img.shields.io/github/commits-since/iotanbo/cpplibhub/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/iotanbo/cpplibhub/compare/v0.0.0...master



.. end-badges

Dependency management tool for C++ and C projects

* Free software: MIT license

Installation
============

::

    pip install cpplibhub

You can also install the in-development version with::

    pip install https://github.com/iotanbo/cpplibhub/archive/master.zip


Documentation
=============


To use the project:

.. code-block:: python

    import cpplibhub
    cpplibhub.longest()


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
