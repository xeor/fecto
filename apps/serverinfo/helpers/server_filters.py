import re
import sys

class ServerFilters:
    '''
    Helpers for the custom filters that can be created to do very specific list filtering
    '''

    loadedFilters = {}

    def getFilterObj(self, filterEntry, request=None):
        filterID = filterEntry['id']

        if not re.match(r'^[a-z]+$', filterID):
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
