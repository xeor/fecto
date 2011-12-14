from django.shortcuts import get_object_or_404

from apps.serverinfo.models import Vlan

class NetworkInfo():
    def getNextIP(self, vlanID):
        try:
            vlanID = int(vlanID)
        except ValueError:
            pass

        if type(vlanID) == int:
            vlanObj = get_object_or_404(Vlan, id=vlanID)
        else:
            vlanObj = vlan

        return vlanObj.getNextAvailableIP()
