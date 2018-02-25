collar-client
#############

|codecov|_ |travis|_ |codacy|_ |rtd|_

Introduction
============

`collar-client` is a local plugin aimed to enrich `dockerd` requests for
`leash-server`.

If your planned rules include relying on clients hostname or containers/images
names, then you'll need to `install collar-client
<http://docker-leash.readthedocs.io/en/latest/install/collar-installation.html>`_
on your machines.

If those are not in your plan, then configure your `dockerd` using `json method
<http://docker-leash.readthedocs.io/en/latest/install/client-installation.html>`_.

.. Warning::
   This is a work in progress.
   Things are not yet stable and are subject to change without notice.

.. |codecov| image:: https://codecov.io/gh/docker-leash/collar-client/branch/master/graph/badge.svg
.. _codecov: https://codecov.io/gh/docker-leash/collar-client

.. |travis| image:: https://travis-ci.org/docker-leash/collar-client.svg?branch=master
.. _travis: https://travis-ci.org/docker-leash/collar-client

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/444467f3204246318ddc8a1af5af89bc
.. _codacy: https://www.codacy.com/app/docker-leash/collar-client?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=docker-leash/collar-client&amp;utm_campaign=Badge_Grade

.. |rtd| image:: https://readthedocs.org/projects/docker-leash/badge/?version=latest
.. _rtd: http://docker-leash.readthedocs.io/en/latest/?badge=latest
