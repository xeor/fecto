import os
import pkgutil
import sys
import re

import apps.serverinfo.attributes
from apps.serverinfo.models import AttributeType

class AttributeClass():
    """
    This class should be inherited by custom attributes which is placed in the 'attributes' folder, with the name
    matching its id_name in the database.
    """

    __author__ = 'No Name <no.name@example.com>'
    __version__ = '1.0'

    def searchInput(self):
        """
        Return the html to render the filter input. The idea is to use a template here..
        """
        return ''

    def searchFilter(self, serverObj, value, keys):
        """
        Should return True/False based on whatever to display or hide this column based on the input filter
        You should always name your returnvalue 'attrfilter_%s' yourFilterName.
        """
        return True # Default

    def toDisplayText(self, textInput):
        """
        Convert your attribute text to something else. Like a number to a word.
        This is for display only..
        """
        return textInput

class AttributeManager():
    attributesObjects = {}
    attributeNames = {}

    def getAttributeObj(self, attributeID):
        if self.attributesObjects.get(attributeID, None):
            return self.attributesObjects[attributeID]

        if re.match(r'^[a-zA-Z0-9_-]+$', attributeID) is None:
            # FIXME: Logger
            return None

        fullImportPath = 'apps.serverinfo.attributes.%s' % attributeID
        try:
            __import__(fullImportPath)
            moduleObj = sys.modules[fullImportPath].Attribute
        except ImportError:
            moduleObj = AttributeClass # Just use our blank one..

        self.attributesObjects[attributeID] = moduleObj
        return moduleObj

    def getModuleNames(self):
        """
        Get a list of all module names.
        """
        if self.attributeNames:
            return self.attributeNames

        self.attributeNames['all'] = [ a.id_name for a in AttributeType.objects.all() ]

        modulePath = os.path.dirname(apps.serverinfo.attributes.__file__)
        self.attributeNames['withcustom'] = [name for modLoader, name, isPkg in pkgutil.iter_modules([modulePath])]
        return self.attributeNames

    def getWithData(self, keys):
        """
        Find out which of our attributes that contains any data. We need this to be able to pick which attribute
        to filter on..
        """
        attrWithData = []
        #possibleAttributes = [ a.replace('attrfilter_', '') for a in keys['columnsVisibleFilterable'].split('.') if a.startswith('attrfilter_') ]
        possibleAttributes = self.getModuleNames()['all']
        for a in possibleAttributes:
            keyName = 'attrfilter_%s' % a
            if not keys.get(keyName):
                continue
            if keys[keyName]:
                attrWithData.append(a)

        return attrWithData