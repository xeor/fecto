import os
import pkgutil
from django_hosts import patterns, host
import apps

host_patterns = patterns('',
    host(r'fecto', 'fecto.urls', name='fecto'),
)


# Automatically accept all hosts as virtual domains as well..
hostsPath = os.path.dirname(apps.__file__)
for modLoader, appName, isPkg in pkgutil.iter_modules([hostsPath]):
    try:
        fullImportPath = 'apps.%s.urls' % appName
        # Just to check
        __import__(fullImportPath)
    except ImportError:
        continue

    host_patterns += patterns('', host(r'^%s(:[0-9]{1,5})?' % appName, fullImportPath, name=appName))
