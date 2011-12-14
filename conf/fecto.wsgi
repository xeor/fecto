import os, sys, site

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(PROJECT_ROOT,'ext/lib/python2.6/site-packages'))
sys.path.insert(0, PROJECT_ROOT)

sys.stdout = sys.stderr

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()