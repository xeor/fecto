from apps.serverinfo.models import AttributeType
from apps.serverinfo.config import statusLevelsDict

class ServerColumns():
    columns = []
    columnsIDs = []
    columnsDict = {}
    attributeColumns = []

    def __init__(self):
        if not self.columns:
            self.populate()

    def populate(self):
        self.columns += self.getNormalColumns()
        self.columns += self.getAttributeColumns()
        self.generateOtherFormats()

    def generateOtherFormats(self):
        for column in self.columns:
            # FIXME, cache stuff here..
            self.columnsIDs.append(column['id'])
            self.columnsDict[column['id']] = column

    def getNormalColumns(self):
        columns = [
            # name            Display name
            # id              Short unique id
            # defaultHidden   Default hidden as a column
            # htmlOptions     Extra html options for column
            # noSort          Column is not sortable
            # noFilter        Column can not be filtered on         # WAS noSearch
            # editable        Editable manually from frontend, and /serverinfo/api/edit api
            # noDB            Datafield which does not come directly from the database
            # filter_path     Filter path when user is searching/filtering
            # separator       Separator to use when several items are returned
            # selectFilter    Use an selectbox instead of text when filtering. (value is a dict)
            {'name': 'ID', 'id': 'id', 'defaultHidden': True, 'htmlOptions': '{"sWidth": "1em"}'},
            {'name': 'Name', 'id': 'name', 'editable':True, 'htmlOptions': '{"sWidth": "15em"}'},
            {'name': 'Function', 'id': 'function', 'editable': True},
            {'name': 'Description', 'id': 'description', 'editable': True},
            {'name': 'Note', 'id': 'note', 'editable': True},
            {'name': 'Virtual', 'id': 'virtual', 'editable': True},
            {'name': 'IP', 'id': 'ip', 'noSort': True, 'separator': ', ', 'filter_path': 'ip__ip__contains', 'editable': True},
            {'name': 'Status', 'id': 'status', 'editable': True, 'selectFilter': statusLevelsDict},
            {'name': 'Registered', 'id': 'reg_time', 'defaultHidden': True},
            {'name': 'Updated', 'id': 'upd_time'},
            {'name': 'Actions', 'id': 'actions', 'noFilter': True, 'noDB': True, 'separator': ' | '},
            ]

        return columns


    def getAttributeColumns(self):
        if self.attributeColumns:
            return self.attributeColumns

        for attribute in AttributeType.objects.all():
            typeDict = {}
            typeDict['name'] = attribute.name
            typeDict['id'] = attribute.id_name
            typeDict['isAttribute'] = True # Must be set
            typeDict['defaultHidden'] = True
            typeDict['noDB'] = True
            typeDict['noFilter'] = True # We cant search yet, no db..
            typeDict['noSort'] = True # Doesnt work yet, it tries to sort via the db..
            self.attributeColumns.append(typeDict)

        return self.attributeColumns
