import simplejson
import re
import datetime
import sys
import os

from django.views.decorators.csrf import csrf_exempt

#from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.conf import settings

from apps.siteconfig.conf import Conf
from apps.serverinfo.models import Server, AttributeMapping, IP
from apps.serverinfo import config
from apps.serverinfo import filters
from apps.serverinfo.helpers import server_columns, form_dynamics

from forms import AddAttributeForm, AddIPForm

# We need this to be included to get the filtering templates to work
filter_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'filters'))
settings.TEMPLATE_DIRS = settings.TEMPLATE_DIRS + (filter_path,)

# Global variables
loadedFilters = {}

# Special simplejson encoder to support ugettext_lazy objects..
# See https://docs.djangoproject.com/en/dev/topics/serialization/#id2
from django.utils.functional import Promise
from django.utils.encoding import force_unicode
class LazyEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return super(LazyEncoder, self).default(obj)

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

    print 'so',serverObj
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
    '''
    This will be appended to the current form depending on
    what the use requests in the first inputfield
    '''
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
    if naming == 'id':
        serverObj = get_object_or_404(Server, id=serverID)
    if naming == 'name':
        serverObj = get_object_or_404(Server, name=serverID)

    attributes_html = getAttributeTableHtml(serverObj)
    network_html = getIpTableHtml(serverObj)
    net_form_helpers = getIpInputHtml(request)

    return render_to_response('serverinfo/details.html', {
            'server': serverObj,
            'attributes_html': attributes_html,
            'network_html': network_html,
            'net_form': AddIPForm,
            'net_form_helpers': net_form_helpers,
            'attr_form': AddAttributeForm,
            }, context_instance=RequestContext(request))


def getFilterObj(filterEntry):
    filterID = filterEntry['id']
    if not re.match(r'^[a-z]+$', filterID):
        return False

    if loadedFilters.get(filterID):
        return loadedFilters[filterID]

    moduleName = 'apps.serverinfo.filters.' + filterID
    __import__(moduleName)

    try:
        filterFunction = getattr(sys.modules[moduleName], 'filter')
    except:
        return False

    filterOutput = {
        'function': sys.modules[moduleName],
        'filter': filterFunction,
        'id': filterID,
        'name': filterEntry['name'],
        'config': filterEntry,
        'template': '%s/template.html' % (filterEntry['id'],),
        }

    loadedFilters[filterID] = filterOutput

    return filterOutput


# FIXME: Take away and take away comment on the detail() view
# function, which adds the cookie.. Most is ready for csrf on js side
@csrf_exempt
def json(request, query_string):
    json_data = {}

    # Populate loadedFilters if its not already loaded
    [ getFilterObj(f) for f in config.filters ]

    # Json requests by filter plugins, a catch all at the end...
    requestedFilter = query_string.split('/')[0]
    if requestedFilter in loadedFilters:
        try:
            jsonFunction = getattr(loadedFilters[requestedFilter]['function'], 'json')
        except:
            return HttpResponseBadRequest()

        json_data = jsonFunction(request)
        return HttpResponse(simplejson.dumps(json_data))

    return HttpResponseBadRequest()

def index(request):
    c = Conf()
    serverColumns = server_columns.ServerColumns()

    columns = c.get('Text', 'usedColumns', 'apps.serverinfo') # was attributes =

    for column in serverColumns.columns:
        if (column['id'] in columns) and (column['id'] in serverColumns.columnsIDs):
            columns[columns.index(column['id'])] = column
        else:
            if column.get('isAttribute', None):
                columns.append(column)

    # Remove all none dicts which is left because we didnt find a match
    [ columns.remove(i) for i in columns if type(i) != dict ]

    filters = []
    for f in config.filters:
        filterObj = getFilterObj(f)
        if not filterObj: continue
        filters.append(filterObj)

    return render_to_response(
        'serverinfo/index.html',
        {
            'columns': columns,
            'filters': filters,
            }
        , context_instance=RequestContext(request))
