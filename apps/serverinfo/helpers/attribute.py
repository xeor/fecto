import sys
import re

class AttributeClass():
    """
    This class should be inherited by custom attributes which is placed in the 'attributes' folder, with the name
    matching its id_name in the database.
    """

    __author__ = 'No Name <no.name@example.com>'
    __version__ = '1.0'

    def searchInput(self):
        pass

    def searchFilter(self):
        pass


class AttributeManager():
    def getAttributeObj(self, attributeID):
        if re.match(r'^[a-zA-Z0-9_-]+$', attributeID) is None:
            # FIXME: Logger
            return None

        fullImportPath = 'apps.serverinfo.attributes.%s' % attributeName
        __import__(fullImportPath)
        return sys.modules[fullImportPath].Attribute
    # FIXME, NEXT: Work this idea into other parts of the site.. ideabase..