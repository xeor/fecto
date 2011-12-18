from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fecto.views.home', name='home'),
    # url(r'^fecto/', include('fecto.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^serverinfo/', include('apps.serverinfo.urls')),


)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)