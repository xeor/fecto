import re
import datetime

from django.db.models import Q
from django.conf import settings

from lib.errors import *

from apps.serverinfo import config as serverinfoConfig
from apps.serverinfo.models import Server, AttributeMapping
from apps.serverinfo.helpers import server_columns, server_filters, attribute

class ServerQuery():
    totalCount = 0 # Populated by handle()
    requestedServerCount = 0 # Populated by handle()

    columnsVisibleFilterable = [] # Populated by handleColumnFilters()
    columnFiltersToUse = [] # Populated by handleColumnFilters()

    pagingStart = None # Populated by handleSorting()
    pagingCount = None # Populated by handleSorting()

    attributesObj = None # Populated in generateDict(), used in generateDataTablesEntry()

    def __init__(self):
        self.serverColumns = server_columns.ServerColumns()
        self.attributesManager = attribute.AttributeManager()

    def applyColumnFilter(self, serversObj, columnFilter, fieldName):
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
        """
        Collects and figure out information we need about the colum filtering. The filtering for each columns in the list.
        """
        re_columnfilter = re.compile(r'^columnfilter_')

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
                if columnFilter in columnsVisibleFilterableRaw:
                    isFilterable = True
                else:
                    isFilterable = False

                columnFilterID = re_columnfilter.sub('', columnFilter)

                if columnFilterID in self.serverColumns.columnsIDs:
                    if isFilterable:
                        self.columnsVisibleFilterable.append(columnFilterID)

                    columnsVisible.append(columnFilterID)

        # A list of all column filters that the user have globally configured to show.
        conf_columnFilters = settings.APPS_SERVERINFO['visible_columns']

        for attributeColumn in self.serverColumns.getAttributeColumns():
            conf_columnFilters.append(attributeColumn['id'])

        self.columnFiltersToUse = []
        [ self.columnFiltersToUse.append(columnFilterName) for columnFilterName in conf_columnFilters if columnFilterName in columnsVisible ]
        if self.columnFiltersToUse == []:
            raise ConfigurationError('No columnFiltersToUse is defined')

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


    def handleMainQuery(self, serversObj):
        query = self.keys.get('sSearch', None)

        q = Q()
        for columnFilter in self.columnsVisibleFilterable:
            # Check the config if we have any special way to filter this field. If not, use __icontains
            filterPath = self.serverColumns.columnsDict[columnFilter].get('filter_path', str(columnFilter) + '__icontains')

            q = q | Q(**{filterPath: query})

        return serversObj.filter(q)


    def handleCustomFilters(self, serversObj):
        """
        Run the trough every custom filters and apply their own filter functions to the serversObj
        """
        serverFilters = server_filters.ServerFilters()
        for customFilter in serverinfoConfig.filters:
            filterObj = serverFilters.getFilterObj(customFilter)
            if filterObj is False: continue

            filteredData = filterObj['filter'](self.keys, serversObj)
            if not filteredData == False:
                serversObj = filteredData

        return serversObj

    def handleSorting(self, serversObj):
        # FIXME, default sorting should be configurable
        sort = self.keys.get('iSortingCols', False)
        self.pagingStart = int(self.keys.get('iDisplayStart', 0))
        self.pagingCount = int(self.keys.get('iDisplayLength', 10))

        # We are supporting many sort fields, so we need to go trough iSortCol_N to find out what to sort
        # Default sort is 'name'
        sortRules = []
        if sort:
            nonSortable = []
            [ nonSortable.append(noSort['id']) for noSort in self.serverColumns.columns if noSort.get('noSort', False) ]

            for i in range(int(sort)):
                sortfieldID = self.keys.get('iSortCol_%s' % (str(i),), False)

                if sortfieldID:
                    # We have a +/- field statically in our table, so we need -1 to match our fields
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
        """
        Take care of all cell data..
        Since the attributes is kinda tricky to filter on, we are also handling that here, while we already
        loops trough the celldata.
        """
        entryData = ['<img src=\"/static/serverinfo/img/details_open.png\" rel="%s">' % serverObj.id]
        for columnFilter in self.columnFiltersToUse:
            if columnFilter in self.attributeNames['all']:

                # We are dealing with an attribute
                if columnFilter in self.attributeNames['withcustom']:
                    # Our attribute have a custom extension in apps.serverinfo.attributes

                    if not self.attributesObj.get(serverObj.id, None):
                        # Skip the whole row if our current attribute contains data which we should filter on
                        if columnFilter in self.attributesWithData: return None

                        # Add nothing if there is no attribute data on this server at all
                        entryData.append('')
                        continue

                    if not self.attributesObj[serverObj.id]['attr'].get(columnFilter, None):
                        if columnFilter in self.attributesWithData: return None

                        # Add nothing if our attribute type is not present for this server.
                        entryData.append('')
                        continue

                    attributeObj = self.attributesManager.getAttributeObj(columnFilter)()
                    attributeData = []

                    for attrValue in self.attributesObj[serverObj.id]['attr'][columnFilter]:
                        # Loop trough every attribute value for each of the attributes for our serverObject
                        # Note that a server can have several attributes of the same type, therefor this loop.
                        if not attributeObj.searchFilter(serverObj, attrValue, self.keys):
                            if columnFilter in self.attributesWithData:
                                # Take away the whole row, but only if the value is anything..
                                return None

                        attributeData.append(attributeObj.toDisplayText(attrValue))

                    entryData.append(', '.join(attributeData))
                else:
                    try:
                        entryData.append( ', '.join(self.attributesObj[serverObj.id]['attr'][columnFilter]) )
                    except KeyError:
                        entryData.append('')

            else:
                # We are dealing with a normal field
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

                if columnData is None:
                    columnData = ''

                # Our columnData should be a string by now..
                if type(columnData) == str or type(columnData) == unicode:
                    entryData.append(columnData)
                else:
                    entryData.append(str(columnData))

        return entryData

    def genAttributeObj(self, servers):
        servers = [ s for s in servers ] # Workaround for bug: <broken repr (DatabaseError:....
        attributesObj = AttributeMapping.objects.select_related().filter(server__in=servers)
        allAttributes = {}
        for attribute in attributesObj:
            serverID = attribute.server_id
            if not allAttributes.get(attribute.server_id, None):
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
            "aaData": [],
            "allIDs": [],
            }

        self.attributesObj = self.genAttributeObj(serversObj)
        self.attributeNames = self.attributesManager.getModuleNames()
        self.attributesWithData = self.attributesManager.getWithData(self.keys)

        for serverEntry in serversObj:
            # Will be None if any filter decides to not show the current item..
            serverDict = self.generateDataTablesEntry(serverEntry)

            if serverDict:
                serversDict['allIDs'].append(str(serverEntry.id))
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
        # NOTE: This function will also handle attributeFiltering. They are not db based
        # and we need to check them after/while they are converted to a dict..
        serversDict = self.generateDict(serversObj)

        # We are ready to count how many items we have..
        serversDict['iTotalDisplayRecords'] = len(serversDict['aaData'])

        # Make sure our newly added server is on the top of our list
        # We don't need to count or do anything special with this. It
        # will get another color as well in the gui (FIXME)
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
        # a freeze list of whats displayed. Not everything that matches
        serversDict['serversCSV'] = ','.join(serversDict['allIDs'])

        # The api framework will take care of converting this into json
        return serversDict

