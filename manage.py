#!/usr/bin/env python
from django.core.management import execute_manager
import imp
try:
    imp.find_module('settings') # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)

import settings

# FIXME
import sys, os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT,'ext/lib/python2.6/site-packages'))
sys.path.insert(0, os.path.join(PROJECT_ROOT,'ext/lib/python2.7/site-packages')) # FIXME: Dirty fix.. Autodetect... :)
sys.path.insert(0, PROJECT_ROOT)

if __name__ == "__main__":
    execute_manager(settings)
