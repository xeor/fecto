import os

#from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.conf import settings
from django.http import Http404

from apps.siteconfig.conf import Conf
from apps.serverinfo.models import Server, AttributeMapping, IP
from apps.serverinfo import config
from apps.serverinfo.helpers import server_columns, form_dynamics, server_filters, attribute

from forms import AddAttributeForm, AddIPForm

# We need this to be included to get the filtering templates to work
filter_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'filters'))
settings.TEMPLATE_DIRS = settings.TEMPLATE_DIRS + (filter_path,)

# Same with attributes
filter_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'attributes'))
settings.TEMPLATE_DIRS = settings.TEMPLATE_DIRS + (filter_path,)

# Special simplejson encoder to support ugettext_lazy objects..
# See https://docs.djangoproject.com/en/dev/topics/serialization/#id2

def getAttributeTableHtml(serverObj):
    attributesObj = AttributeMapping.objects.filter(server=serverObj).order_by('attributeType__name')
    count = attributesObj.count()

    if count != 0:
        html = render_to_string(
            'serverinfo/attributes_html.html',
                {
                'attributes': attributesObj,
                'server': serverObj,
                }
        )
    else:
        html = None

    return html

def getIpTableHtml(serverObj):
    networkObj = IP.objects.filter(server=serverObj)
    count = networkObj.count()

    if count != 0:
        html = render_to_string(
            'serverinfo/network_html.html',
                {
                'ips': networkObj,
                'server': serverObj,
                }
        )
    else:
        html = None

    return html

def getIpInputHtml(request):
    """
    This will be appended to the current form depending on
    what the use requests in the first inputfield
    """
    formDynamicsObj = form_dynamics.IPFormDynamics()

    inputs = formDynamicsObj.getFilters(request)

    html = render_to_string(
        'serverinfo/network_extraform.html',
            {
            'inputs': inputs,
            }
    )

    return html

# FIXME: Take away csrf_excempt when django ensure_csrf_cookie is in a
# stable version! Its not in 1.3.1. JS request stuff is ready..
#@ensure_csrf_cookie
def details(request, serverID, naming='id'):
    serverObj = None
    if naming == 'id':
        serverObj = get_object_or_404(Server, id=serverID)
    if naming == 'name':
        serverObj = get_object_or_404(Server, name=serverID)

    if not serverObj:
        raise Http404
    attributes_html = getAttributeTableHtml(serverObj)
    network_html = getIpTableHtml(serverObj)
    net_form_helpers = getIpInputHtml(request)

    return render_to_response('serverinfo/details.html', {
        'server': serverObj,
        'attributes_html': attributes_html,
        'network_html': network_html,
        'net_form': AddIPForm,
        'net_form_helpers': net_form_helpers,
        'attr_form': AddAttributeForm(serverID=serverID),
        }, context_instance=RequestContext(request))


def index(request):
    c = Conf()
    serverColumns = server_columns.ServerColumns()
    serverFilters = server_filters.ServerFilters()
    attributeManager = attribute.AttributeManager()

    columns = c.get('Text', 'usedColumns', 'apps.serverinfo') # was attributes =
    attributeFilters = {}

    for column in serverColumns.columns:
        if (column['id'] in columns) and (column['id'] in serverColumns.columnsIDs):
            columns[columns.index(column['id'])] = column
        else:
            if column.get('isAttribute', None):
                currentAttributeObj = attributeManager.getAttributeObj(column['id'])()
                attributeFilters[column['id']] = currentAttributeObj.searchInput()
                columns.append(column)

    # Remove all none dicts which is left because we didn't find a match
    [columns.remove(i) for i in columns if type(i) != dict]

    filters = []
    for f in config.filters:
        filterObj = serverFilters.getFilterObj(f, request=request)
        if not filterObj: continue
        filters.append(filterObj)

    return render_to_response(
        'serverinfo/index.html',
            {
            'columns': columns,
            'filters': filters,
            'attributeFilters': attributeFilters,
            }
        , context_instance=RequestContext(request))
