from django.conf.urls.defaults import *

from djangorestframework.views import ListOrCreateModelView, InstanceModelView

from django.conf.urls.defaults import patterns

from apps.serverinfo.api import RootResource, ServerResource, ServerResourceQuery, \
    ServerInlineFormResource, AttributeResource, ServerGetInfoResource, ServerNewResource, \
    AttributesResource, getIpHelperFormsResource, getNextIpResource, IpResource, NoteResource, \
    filterAjaxResource

urlpatterns = patterns('',
                       url(r'^$', RootResource.as_view()),

                       url(r'^server/$', ListOrCreateModelView.as_view(resource=ServerResource), name='server-resource'),
                       url(r'^server/get/', ServerGetInfoResource.as_view()),
                       url(r'^server/new/', ServerNewResource.as_view()),
                       url(r'^server/datatables/', ServerResourceQuery.as_view()),
                       url(r'^server/inlineForm/', ServerInlineFormResource.as_view()),
                       url(r'^server/attribute/', AttributeResource.as_view()),
                       url(r'^server/ip/', IpResource.as_view()),
                       url(r'^server/note/', NoteResource.as_view()),
                       url(r'^server/(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=ServerResource)),

                       url(r'^attributes/$', ListOrCreateModelView.as_view(resource=AttributesResource), name='attributes-resource'),
                       url(r'^attributes/(?P<pk>[^/]+)/$', InstanceModelView.as_view(resource=AttributesResource)),
                       url(r'^getIpHelperForms/$', getIpHelperFormsResource.as_view()),
                       url(r'^getIpHelperNext/$', getNextIpResource.as_view()),
                       url(r'^filter/(?P<filterName>[a-z0-9_-]+)/', filterAjaxResource.as_view()),
                       )

# Static views served by the rest framework itself
urlpatterns = urlpatterns + patterns('djangorestframework.utils.staticviews',
                                     (r'robots.txt', 'deny_robots'),
                                     (r'favicon.ico', 'favicon'),
                                     (r'^accounts/login/$', 'api_login'),
                                     (r'^accounts/logout/$', 'api_logout'),
)
