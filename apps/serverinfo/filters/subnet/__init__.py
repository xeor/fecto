from apps.serverinfo.views import getIpInputHtml

from apps.serverinfo.models import Vlan
from apps.contact.models import Location

name = 'Subnet/Vlan'

def filter(keys, dbObj):
    '''
    This function will run even if the filter is not visible, so you can make all kind of filters.
    If the data for your filter is not in the "keys" variable you should return False (or nothing)!
    Else, return dbObj in the modified form you want..
    '''

    if not keys['filter_subnet_value']:
        return False

    rawData = keys['filter_subnet_value']
    data = dict([ i.split('-') for i in rawData.split(',') if i ])

    if data.get('location', False):
        locationID = int(data['location'])
        if locationID == 0: # * No location * is selected
            dbObj = dbObj.filter(ip__vlan__location=None)
        else:
            locationObj = Location.objects.get(id=locationID)
            dbObj = dbObj.filter(ip__vlan__location=locationObj)

        if data.get('vlan', False):
            vlanID = data['vlan']
            vlanObj = Vlan.network_objects.get(id=vlanID)
            dbObj = dbObj.filter(ip__vlan=vlanObj)

        return dbObj

    return False

def templateDict(request):
    '''
    Will be accessible as {{ data }} in your template.
    Remember that this can be a dict or whatever you want
    but the data will loaded at page load, not when you open
    the filter!
    '''

    form = getIpInputHtml(request)
    return {'form': form}
