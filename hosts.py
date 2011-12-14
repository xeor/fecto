from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'^serverinfo(:[0-9]{1,5})?', 'apps.serverinfo.urls', name='serverinfo'),
    host(r'fecto', 'fecto.urls', name='fecto'),
)
