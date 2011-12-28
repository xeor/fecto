.. meta::
   :description: From Eternal Chaos To Order
   :keywords: django, python, management, server, serverinfo

Fecto's documentation
=====================

Introduction
------------

This project is in alpha stage, and should not be used yet.

Its job will be to manage servers, ip's, and groups in an easy to work with manner.
The project is built using Django, and based on "need to have" features. It tries to
be as customizable as possible to make it easy to add new "need to have" features.

Resources
---------

* Project hosting `GitHub <https://github.com/xeor/fecto>`_.
* Bug reports are handled on the `issue tracker <https://github.com/xeor/fecto/issues>`_.

Any questions, thoughts, bugs are very welcome!


Requirements
------------

* Python (2.6, 2.7 supported)


Installation
------------

If you really want to try it, despite, its in (common use alpha), here is some notes.

* Make sure that pip is installed
* Make sure you have installed virtualenv (pip install virtualenv)
* Redis should be installed and running..
* mkdir -p static/CACHE/{css,js}
* python setup/bootstrap.py
* source ext/bin/activate   # If script runned ok..
* python setup/bootstrap.py # This time, inside the virtualenv :)


Applications
------------

The only application which is currently available is the serverinfo
app. Other apps will be created later.


.. toctree::
  :maxdepth: 1

  apps/serverinfo
  apps/messages
  apps/diskoverview


FAQ
---

* Why the name "Fecto", and what does it mean?

  * Fecto stands for (From Eternal Chaos To Order).

* You didnt say why...

  * You have probably worked at, atleast one company that uses excel to keep track of servers/ip's.. Hence, the chaos. Fecto will make order :)
  * Not only for serverinfo tough.. Other small "apps" will be created in this project to create even more order.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

