import re
import datetime

from django.db.models import Q

from apps.siteconfig.conf import Conf
from apps.serverinfo import config as serverinfoConfig
from apps.serverinfo.models import Server, AttributeMapping
from apps.serverinfo.helpers import server_columns, server_filters

class ServerQuery():
    totalCount = 0 # Populated by handle()
    requestedServerCount = 0 # Populated by handle()

    columnsVisibleFilterable = [] # Populated by handleColumnFilters()
    columnFiltersToUse = [] # Populated by handleColumnFilters()

    pagingStart = None # Populated by handleSorting()
    pagingCount = None # Populated by handleSorting()

    #loadedFilters = {} # Populated by getFilterObj()

    attributesObj = None # Populated in generateDict(), used in generateDataTablesEntry()

    def __init__(self):
        self.serverColumns = server_columns.ServerColumns()

    def applyColumnFilter(self, serversObj, columnFilter, fieldName):
        #filterPath = self.serverColumns.columnsDict[columnFilter].get('filter_path', str(columnFilter) + '__icontains')

        try:
            if columnFilter == 'NONE':
                # We need to use a variable in our filter query, therefor we need to do the **{fieldName: ...} hack.
                # Normal is .filter('system__name__icontains=something')
                serversObj = serversObj.filter(**{str(fieldName): None})
            else:
                filterPath = self.serverColumns.columnsDict[fieldName].get('filter_path', str(fieldName) + '__icontains')
                serversObj = serversObj.filter(**{filterPath: columnFilter})
        except KeyError:
            pass

        return serversObj


    def handleColumnFilters(self, serversObj):
        '''
        Collects and figure out information we need about the colum filtering. The filtering for each columns in the list.
        '''
        configObj = Conf()
        #visibleColumnFiltersRaw = self.keys.get('visibleColumnFilters', '').split('.')
        re_columnfilter = re.compile(r'^columnfilter_')
        #requestedColumnFilters = []

        # Generate a list of every columns with the html class
        # .search_init (which are the columns which we can filter on)
        columnsVisibleFilterableRaw = self.keys.get('columnsVisibleFilterable','').split('.')

        # Will be populated with a list of all columns visible
        columnsVisible = []

        for columnFilter in self.keys:
            # We haveto loop trough and find every columnfilter_ here, even those who doesnt have
            # a search/filter option. Eg the action filter doesnt have this, but needs to be
            # a part of columnsVisible to make sure we are returning the right amount of fields
            # back to the table at the end..
            if columnFilter.startswith('columnfilter_'):
                #if columnFilter in visibleColumnFiltersRaw:
                if columnFilter in columnsVisibleFilterableRaw:
                    isFilterable = True
                else:
                    isFilterable = False

                columnFilterID = re_columnfilter.sub('', columnFilter)

                if columnFilterID in self.serverColumns.columnsIDs:
                    if isFilterable:
                        #self.visibleColumnFilters.append(columnFilterID)
                        self.columnsVisibleFilterable.append(columnFilterID)

                    columnsVisible.append(columnFilterID)

        # A list of all column filters that the user have globally configured to show.
        conf_columnFilters = configObj.get('Text', 'usedColumns', 'apps.serverinfo')

        for attributeColumn in self.serverColumns.getAttributeColumns():
            conf_columnFilters.append(attributeColumn['id'])

        self.columnFiltersToUse = []
        [ self.columnFiltersToUse.append(columnFilterName) for columnFilterName in conf_columnFilters if columnFilterName in columnsVisible ]

        columnFilters = {}
        nonSearchable = []
        [ nonSearchable.append(noSearch['id']) for noSearch in self.serverColumns.columns if noSearch.get('noFilter', False) ]

        for columnFilter in self.columnFiltersToUse:
            requestedColumnFilter = self.keys.get('columnfilter_%s' % (columnFilter,), False)

            if not requestedColumnFilter:
                continue

            if columnFilter in nonSearchable:
                continue

            columnFilters[columnFilter] = requestedColumnFilter


        for columnFilter in columnFilters:
            serversObj = self.applyColumnFilter(serversObj, columnFilters[columnFilter], columnFilter)

        return serversObj


    def handleMainQuery(self, serversObj): # WAS searchHandlerSearchFilter
        # FIXME, not implemented, name ORing function

        # request -> query
        # serverListObj -> serversObj
        # attrToUse -> self.columnFiltersToUse
        # visibleAttr -> self.visibleColumnFilters

        # filter_main -> query
        # filter_main = request.REQUEST.get('sSearch', False) # Main filter (top right)

        query = self.keys.get('sSearch', None)

        q = Q() # WAS qObj
        for columnFilter in self.columnsVisibleFilterable: # vAttr -> columnFilter
            # Check the config if we have any special way to filter this field. If not, use __icontains

            filterPath = self.serverColumns.columnsDict[columnFilter].get('filter_path', str(columnFilter) + '__icontains')

            q = q | Q(**{filterPath: query})

        #import ipdb; ipdb.set_trace()
        # FIXME: Q contains OR: (AND,).... ????

        return serversObj.filter(q)


    def handleCustomFilters(self, serversObj):
        '''
        Run the trough every custom filters and apply their own filter functions to the serversObj
        '''
        serverFilters = server_filters.ServerFilters()
        for customFilter in serverinfoConfig.filters:
            filterObj = serverFilters.getFilterObj(customFilter)
            if filterObj == False: continue
            filterID = filterObj['id']

            filteredData = filterObj['filter'](self.keys, serversObj)
            if not filteredData == False:
                serversObj = filteredData

        return serversObj

    def handleSorting(self, serversObj):
        # FIXME, maybe some issues when sorting on secondary fields
        # FIXME, default sorting should be configurable
        sort = self.keys.get('iSortingCols', False)
        self.pagingStart = int(self.keys.get('iDisplayStart', 0))
        self.pagingCount = int(self.keys.get('iDisplayLength', 10))

        if self.pagingCount == -1:
            self.pagingCount = serverCount

        # We are supporting many sort fields, so we need to go trough iSortCol_N to find out what to sort
        # Default sort is 'name'
        sortRules = []
        if sort:
            nonSortable = []
            [ nonSortable.append(noSort['id']) for noSort in self.serverColumns.columns if noSort.get('noSort', False) ]

            for i in range(int(sort)):
                sortfieldID = self.keys.get('iSortCol_%s' % (str(i),), False)

                if sortfieldID:
                    # We have a +/- field staticly in our table, so we need -1 to match our fields
                    sortfield = self.columnFiltersToUse[int(sortfieldID) - 1]

                    if sortfield:
                        if sortfield in nonSortable:
                            continue

                        sortdirection = self.keys.get('sSortDir_%s' % (str(i),))
                        if sortdirection == 'desc':
                            sortRules.append('-%s' % sortfield)
                        else:
                            sortRules.append(sortfield)

        else:
            sortRules.append('name')

        return serversObj.order_by(*sortRules)

    def handleManualGETs(self, serversObj):
        freezeByID = self.keys.get('extra_freezeByID', None)

        if freezeByID:
            frozenIDs = freezeByID.split(',')
            serversObj = serversObj.filter(id__in=frozenIDs)

        return serversObj

    def generateDataTablesEntry(self, serverObj):
        entryData = []
        entryData.append('<img src=\"/static/serverinfo/img/details_open.png\" rel="%s">' % serverObj.id) # First entry is +/- image
        for columnFilter in self.columnFiltersToUse:
            try:
                columnData = getattr(serverObj, columnFilter)
                # Special handlers for different types of data that can end up in a column
                if callable(columnData):
                    # Lets check if its a function first, in case it returns something we need to take care of
                    columnData = columnData()

                if type(columnData) == datetime.datetime:
                    columnData = str(columnData)

                if hasattr(columnData, 'all'): # This is a many2many field
                    # FIXME, config separator
                    columnData = ', '.join([ str(s) for s in columnData.all() ])

                if type(columnData) == list:
                    # FIXME, config separator
                    columnData = ', '.join(columnData)

                if columnData == None:
                    columnData = ''

                # Our columnData should be a string by now..
                if type(columnData) == str or type(columnData) == unicode:
                    entryData.append(columnData)
                else:
                    entryData.append(str(columnData))
                    #entryData.append('* Unknown data *')

            except AttributeError:
                # We are probably dealing with an attribute since normal database query failed.
                # 1 query per foreignkey name.... FIXME
                #attributeData = serverObj.attributes.filter(name__name=columnFilter)
                #output = ', '.join([ unicode(a) for a in attributeData ])

                #myAttributes = self.attributesObj.filter(server=serverObj)
                #curAttribute = myAttributes.filter(attributeType__id_name=columnFilter)
                #output = ', '.join([ unicode(attr) for attr in curAttribute ]) 

                if not self.attributesObj.get(serverObj.id, None):
                    entryData.append('')
                    continue

                if not self.attributesObj[serverObj.id]['attr'].get(columnFilter, None):
                    entryData.append('')
                    continue

                entryData.append( ', '.join(self.attributesObj[serverObj.id]['attr'][columnFilter]) )
                #entryData.append('* Error handeling datafield *')
                

        return entryData

    def genAttributeObj(self, servers):
        servers = [ s for s in servers ] # Workaround for bug: <broken repr (DatabaseError:....
        attributesObj = AttributeMapping.objects.select_related().filter(server__in=servers)

        allAttributes = {}
        for attribute in attributesObj:
            if not allAttributes.get(attribute.server_id, None):
                serverID = attribute.server_id
                allAttributes[serverID] = {}
                allAttributes[serverID]['attr'] = {}
                allAttributes[serverID]['servername'] = attribute.server.name

            if not allAttributes[serverID]['attr'].get(attribute.attributeType.id_name, None):
                allAttributes[serverID]['attr'][attribute.attributeType.id_name] = []

            allAttributes[serverID]['attr'][attribute.attributeType.id_name].append(attribute.attributeValue.value)

        return allAttributes

    def generateDict(self, serversObj):
        serversDict = {
            "sEcho": self.keys.get('sEcho', 1),
            "iTotalRecords": self.totalCount,
            "iTotalDisplayRecords": self.requestedServerCount,
            "aaData": []
            }

        #self.attributesObj = AttributeMapping.objects.select_related().filter(server__in=serversObj)

        self.attributesObj = self.genAttributeObj(serversObj)

        for serverEntry in serversObj:
            serverDict = self.generateDataTablesEntry(serverEntry)

            if serverDict:
                serversDict['aaData'].append(serverDict)

        return serversDict



    def handle(self, serversObj, keys):
        self.totalCount = serversObj.count()
        self.keys = keys

        serversObj = serversObj.exclude(status=6)

        serversObj = self.handleManualGETs(serversObj)
        serversObj = self.handleColumnFilters(serversObj)
        serversObj = self.handleMainQuery(serversObj)
        serversObj = self.handleCustomFilters(serversObj)
        serversObj = self.handleSorting(serversObj)

        # Filter out dupes which we might have because of many2many relations
        serversObj = serversObj.distinct()

        self.requestedServerCount = serversObj.count()

        # Only grab whatever requested.
        serversObj = serversObj[self.pagingStart:self.pagingStart + self.pagingCount]

        # Take our list and all other information we currently have,
        # and generate a dict in the format that our datatable wants it
        serversDict = self.generateDict(serversObj)

        # Make sure our newly added server is on the top of our list
        # We dont need to count or do anything special with this. It
        # will get another color as well in the gui
        newServer = keys.get('newserver', None)
        if newServer:
            try:
                serverObj = Server.objects.get(name=newServer)
            except Server.DoesNotExist:
                serverObj = None
            if serverObj:
                serversDict['aaData'] = [self.generateDataTablesEntry(serverObj),] + serversDict['aaData']

        # List used by the "freeze list" link, which makes us able to
        # freeze the current displayed list of servers, and filter on
        # that list as well.. This is placed here because we only want
        # a freeze list of whats displayed. Not everything that matces
        serversDict['serversCSV'] = ','.join( [ str(s.id) for s in serversObj ] )

        # The api framework will take care of converting this into json
        return serversDict

