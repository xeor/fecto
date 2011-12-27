import re
import sys

class ServerFilters:
    '''
    Helpers for the custom filters that can be created..
    '''

    loadedFilters = {}

    def getFilterObj(self, filterEntry):
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

        filterOutput = {
            'function': sys.modules[moduleName],
            'filter': filterFunction,
            'id': filterID,
            'name': filterEntry['name'],
            'config': filterEntry,
            'template': '%s/template.html' % (filterEntry['id'],),
            }

        self.loadedFilters[filterID] = filterOutput

        return filterOutput
