from django.conf.urls.defaults import *

from apps.serverinfo import api_urls

urlpatterns = patterns('',
                       url(r'^$', 'apps.serverinfo.views.index', name='serverinfo-root'),

                       url(r'^details/(?P<serverID>[0-9]*)$', 'apps.serverinfo.views.details', {'naming': 'id'}),
                       url(r'^details/(?P<serverID>[0-9a-zA-Z _-]*)$', 'apps.serverinfo.views.details', {'naming': 'name'}),

                       url(r'^json/(.*)$', 'apps.serverinfo.views.json'), # FIXME, use the one below instead..
                       url(r'^api/', include(api_urls)),
                       #url(r'^get/(.*)$', 'apps.serverinfo.views.getone'),
                       #url(r'^export/(.*)$', 'apps.serverinfo.views.export'),

                       )
