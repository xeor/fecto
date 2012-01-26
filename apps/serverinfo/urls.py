from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from apps.serverinfo import api_urls

urlpatterns = patterns('',
                       url(r'^$', 'apps.serverinfo.views.index', name='serverinfo-root'),

                       url(r'^details/(?P<serverID>[0-9]*)$', 'apps.serverinfo.views.details', {'naming': 'id'}),
                       url(r'^details/(?P<serverID>[0-9a-zA-Z _-]*)$', 'apps.serverinfo.views.details', {'naming': 'name'}),
                       url(r'^api/', include(api_urls)),
                       #url(r'^get/(.*)$', 'apps.serverinfo.views.getone'),
                       #url(r'^export/(.*)$', 'apps.serverinfo.views.export'),
)

urlpatterns += staticfiles_urlpatterns()
