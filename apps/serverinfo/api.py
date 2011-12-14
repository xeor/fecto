from django.core.urlresolvers import reverse

from djangorestframework.resources import ModelResource
from djangorestframework.views import View
from djangorestframework.renderers import BaseRenderer, DEFAULT_RENDERERS

from apps.serverinfo.models import Server, AttributeMapping
from apps.serverinfo.views import getIpInputHtml
from apps.serverinfo.helpers import server_query, server_field, network_info

class HTMLRenderer(BaseRenderer):
    """
    Basic renderer which just returns the content without any further serialization.
    """
    media_type = 'text/raw'

class RootResource(View):
    def get(self, request):
        return [
            {'name': 'AttributeMapping', 'url': reverse('attributes-resource')},
            {'name': 'Server', 'url': reverse('server-resource')},
            ]

class AttributesResource(ModelResource):
    model = AttributeMapping

class ServerResource(ModelResource):
    # FIXME: Post doesnt work because of m2m relations. Using an own
    # server/new api call instead for now..
    model = Server

class ServerResourceQuery(View):
    '''
    Query the server list with custom filters.
    '''
    def get(self, request):
        serverQueryHandler = server_query.ServerQuery()
        serversDict = serverQueryHandler.handle(Server.objects.all(), request.GET)

        return serversDict

class ServerInlineFormResource(View):
    '''
    Get field information from a server in a format that we need for use with inline editing.
    '''
    renderers = DEFAULT_RENDERERS + (HTMLRenderer,)

    def get(self, request):
        if not request.GET.get('id', None):
            return {}

        serverInlineForm = server_field.ServerInlineForm()
        inlineFormDict = serverInlineForm.getInlineFormData(request.GET)

        return inlineFormDict

    def post(self, request):
        if not request.POST.get('id', None):
            return {}

        serverInlineForm = server_field.ServerInlineForm()
        inlineFormEntry = serverInlineForm.editInlineFormData(request.POST)

        return inlineFormEntry

class ServerGetInfoResource(View):
    '''
    Gets different custom small information snippets..
    Nothing in here yet.. Just a placeholder/idea holder

    Can grab stuff without authentication for example:
      * Servercount
      * Last server
      * Server with OS equuals to something... (maybe not here..?)
    '''

    renderers = DEFAULT_RENDERERS + (HTMLRenderer,)

    def get(self, request):
        getType = request.GET.get('type', None)

        if getType == 'some type':
            return 'info'

        return {}

class AttributeResource(View):
    '''
    Handle attributes added/removed from servers
    '''

    def get(self, request):
        serverInlineForm = server_field.ServerInlineForm()

        if 'remove' in request.GET:
            status = serverInlineForm.removeAttribute(request.GET)
            return status

        return {}

    def post(self, request):
        serverInlineForm = server_field.ServerInlineForm()
        attributeData = serverInlineForm.addAttribute(request.POST)

        return attributeData

class ServerNewResource(View):
    '''
    Add a new basic server and return its ID
    '''

    def post(self, request):
        serverObj = Server()
        serverName = 'server-%s' % str(Server.objects.latest('id').id + 1)
        serverObj.name = serverName
        serverObj.status = 6 # Hidden
        serverObj.save()
        return serverObj.name

class IpResource(View):
    '''
    Handle IP's added/removed on servers
    '''

    def get(self, request):
        serverInlineForm = server_field.ServerInlineForm()

        if 'remove' in request.GET:
            status = serverInlineForm.removeIP(request.GET)
            return status

        if 'check' in request.GET:
            status = serverInlineForm.checkIP(request.GET)
            return status

        return {}

    def post(self, request):
        serverInlineForm = server_field.ServerInlineForm()
        IpData = serverInlineForm.addIP(request.POST)
        return IpData

class getIpHelperFormsResource(View):
    '''
    Get the next filter we uses in the details view
    '''

    renderers = DEFAULT_RENDERERS + (HTMLRenderer,)

    def get(self, request):
        html = getIpInputHtml(request)
        return html

class getNextIpResource(View):
    '''
    Gets the next available ip for a vlan
    '''

    renderers = DEFAULT_RENDERERS + (HTMLRenderer,)

    def get(self, request):
        vlanID = request.GET.get('filter_vlan', None)
        return network_info.NetworkInfo().getNextIP(vlanID)
