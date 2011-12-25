Fecto
=====

Info
----

This project is in alpha stage, and should not be used yet.

Its job will be to manage servers, ip's, and groups in an easy to work with manner.
The project is built using Django, and based on "need to have" features. It tries to
be as customizable as possible to make it easy to add new "need to have" in your organization.


Features
--------

* Ajax frontpage
  * Filtering (based on logic)
  * Filtering (based on columns search)
  * Main search (OR search for all columns displayed)
  * Sort
  * Export list to different formats (xls, csv, clipboard, print)
  * Detail dropdown for servers
  * Dynamic display of columns
  * Dynamic columns for extra info or tools (actions)
  * Attributes per server
  * Easy add/edit servers. Inline editing..
* Lots of configuration options


Features (to come)
------------------

* "Browse" mode to browse trough field relations
* API
  * Integration with puppet external nodes
  * Add new servers
  * Info about servers returned in different formats
* Importer/exporters
  * Import from xls, txt or others
* Lots more!


Future apps
------------
This application will have more sub-apps than just server information, but serverinfo will be
in focus and will be made first. Later sub-apps that will probably come is:

* Message-web
  * Made to display messages on 24/7 monitors.
  * Will handle network dropouts without displaying a "page not found" message.
  * Refreshes only the message part of the web, so no flickering.
  * Support displaying messages to different groups
  * Groups can have private messages
  * Events happening on different event "rules". Eg send a mail to someone..
  * Much more

* Disk-overview
  * Uses RRD databases (round-robin-database) to get and display disk usage for network volumes
  * Gives warnings when there is less than X mb left.
  * Gives warnings when there is used more than X mb the last minute/hours/24 hours..
  * Can automaticly add all DFS shares under \\domain\dfs..
  * Uses a windows powershell service script as a "slave"
  * Support novell shares

* Probably more..

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

FAQ
---

* Why the name "Fecto", and what does it mean?
  * Fecto stands for (From Eternal Chaos To Order).

* You didnt say why...
  * You have probably worked at, atleast one company that uses excel to keep track of servers/ip's.. Hence, the chaos. Fecto will make order :)
  * Not only for serverinfo tough.. Other small "apps" will be created in this project to create even more order.
