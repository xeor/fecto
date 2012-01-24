import re
from django.template.loader import render_to_string

from apps.serverinfo.helpers.attribute import AttributeClass

class Attribute(AttributeClass):
    def __init__(self):
        self.convertText = re.compile(r'') # FIXME

    def searchFilter(self, serverObj, value, keys):
        if keys.get('attrfilter_ha', None):
            myValue = keys['attrfilter_ha']
        else:
            return False

        if myValue == value:
            return True

        return False

    def searchInput(self):
        html = render_to_string(
            'ha/input.html',
                {
                }
        )

        return html

    def toDisplayText(self, textInput):
        return textInput.replace('yes', 'jepp<b>asd</b>')