import os
import pkgutil
import re
import sys

import apps.serverinfo.filters

class ServerFilters:
    '''
    Helpers for the custom filters that can be created to do very specific list filtering
    '''

    loadedFilters = {}
    filters = []

    def getFilterNames(self):
        if self.filters:
            return self.filters

        modulePath = os.path.dirname(apps.serverinfo.filters.__file__)
        for modLoader, name, isPkg in pkgutil.iter_modules([modulePath]):
            fullImportPath = 'apps.serverinfo.filters.%s' % name
            try:
                __import__(fullImportPath)
                moduleObj = sys.modules[fullImportPath]
                self.filters.append({'name': moduleObj.name, 'id': name})
            except ImportError:
                print 'error importing', fullImportPath
                # FIXME: Log error..
                continue

        return self.filters

    def getFilterObj(self, filterEntry, request=None):
        filterID = filterEntry['id']

        if not re.match(r'^[a-zA-Z_-]+$', filterID):
            # FIXME, log
            return False

        if self.loadedFilters.get(filterID):
            return self.loadedFilters[filterID]

        moduleName = 'apps.serverinfo.filters.' + filterID
        __import__(moduleName)

        try:
            filterFunction = getattr(sys.modules[moduleName], 'filter')
        except AttributeError:
            return False

        try:
            templateDictObj = getattr(sys.modules[moduleName], 'templateDict')
            templateDict = templateDictObj(request)
        except AttributeError:
            templateDict = None

        filterOutput = {
            'function': sys.modules[moduleName],
            'filter': filterFunction,
            'id': filterID,
            'name': filterEntry['name'],
            'config': filterEntry,
            'templateDict': templateDict, # Additional dict sent to the template
            'template': '%s/template.html' % (filterEntry['id'],),
            }

        self.loadedFilters[filterID] = filterOutput

        return filterOutput
