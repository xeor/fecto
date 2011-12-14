from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'^serverinfo', 'apps.serverinfo.urls', name='serverinfo'),
    host(r'fecto', 'fecto.urls', name='fecto'),
)
