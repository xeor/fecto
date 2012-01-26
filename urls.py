import os
import pkgutil
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

import apps

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fecto.views.home', name='home'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

# Include urls files from all apps automatically
urlsPath = os.path.dirname(apps.__file__)
for modLoader, appName, isPkg in pkgutil.iter_modules([urlsPath]):
    try:
        fullImportPath = 'apps.%s.urls' % appName
        # Just to check
        __import__(fullImportPath)
    except ImportError:
        continue

    urlpatterns += patterns('', url('^%s/' % appName, include(fullImportPath)))


# In case our webserver doesnt do this for us
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
