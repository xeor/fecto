from django.shortcuts import get_object_or_404

from apps.serverinfo.models import Vlan

class NetworkInfo():
    def getNextIP(self, vlanID):
        try:
            vlanID = int(vlanID)
        except ValueError, TypeError:
            vlanID = None

        if type(vlanID) == int:
            vlanObj = get_object_or_404(Vlan, id=vlanID)
        else:
            return ''

        return vlanObj.getNextAvailableIP()
