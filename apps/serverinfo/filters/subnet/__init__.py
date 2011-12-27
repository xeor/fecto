#!/usr/bin/env python

from apps.serverinfo.views import getIpInputHtml

def filter(input, dbObj):
    # FIXME, not done at all!

    return dbObj.filter(name__icontains=input['value'])

def ajax(request):
    return 'some ajax text'

def render(request):
    pass
