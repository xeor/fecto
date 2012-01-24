from django import template

from apps.serverinfo.helpers import field_parser

register = template.Library()

def parseStatus(value):
    return field_parser.status(value)
register.filter('parseStatus', parseStatus)

def parseSharedIPs(ips, server):
    #import ipdb; ipdb.set_trace()
    if ips.count <= 1:
        return ''

    sharedServers = []
    for s in ips: # ips contains a list of serverobjects!
        if s == server:
            continue
        serverStr = unicode(s) # FIXME, LINK
        sharedServers.append(serverStr)
    return ', '.join(sharedServers)

register.filter('parseSharedIPs', parseSharedIPs)

def getAttributeFilter(attributeID, attributeFilters):
    if not attributeFilters.get(attributeID, None):
        return ''

    attributeFilterHtml = attributeFilters[attributeID]

    if not attributeFilterHtml:
        return ''

    return attributeFilterHtml
register.filter('getAttributeFilter', getAttributeFilter)