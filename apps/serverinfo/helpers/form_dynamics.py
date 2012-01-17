
from apps.serverinfo.models import Vlan
from apps.contact.models import Location


class IPFormDynamics():
    def getFilters(self, request):
        inputs = []

        # Location or first and only vlan (if no locations)
        filterItems, filterType = self.getFilter1(request)
        inputs.append({'id': 'filter1', 'type': filterType, 'options': filterItems})

        if filterType == 'vlan':
            inputs[0]['name'] = 'VLan/Subnet'
            return inputs

        if filterType == 'location':
            inputs[0]['name'] = 'Location'
            inputs.append({
                    'id': 'filter_vlan',
                    'options': self.getFilter2(request),
                    'name': 'VLan/Subnet',
                    'type': 'vlan'})

        return inputs

    def getFilter2(self, request):
        '''
        The second filter, which is always vlan.. (location is sat)
        '''

        filterItems = {}

        selectedLocation = request.GET.get('filter1', None)
        if not selectedLocation:
            return {} # Something is wrong..

        selectedLocation = int(selectedLocation)

        if selectedLocation == 0:
            vlansObj = Vlan.network_objects.filter(location__isnull=True)
        else:
            locationObj = Location.objects.get(id=selectedLocation)
            vlansObj = Vlan.network_objects.filter(location=locationObj)

        for vlan in vlansObj:
            filterItems[vlan.id] = {'name': vlan.name, 'selected': ''}

        filterVlanSelected = request.GET.get('filter_vlan', 0)
        if filterVlanSelected == '':
            filterVlanSelected = 0

        filterVlanSelected = int(filterVlanSelected)
        if filterItems.get(filterVlanSelected, None):
            filterItems[filterVlanSelected]['selected'] = 'selected'

        return filterItems

    def getFilter1(self, request):
        '''
        The first filter, which could be locations, or a list of vlans.
        This filter is always displayed
        '''

        filterItems = {}
        vlansObj = Vlan.network_objects.all()

        if vlansObj.filter(location__isnull=False):
            # We have one or more locations which have a location
            filterType = 'location'

            if vlansObj.filter(location__isnull=True):
                # We have one or more location where location is empty
                filterItems[0] = {'name': '* No location *', 'selected': ''}

            for loc in Location.objects.all():
                filterItems[loc.id] = {'name': loc.name, 'selected': ''}
        else:
            filterType = 'vlan'
            for vlan in vlansObj.order_by('name'):
                filterItems[vlan.id] = {'name': vlan.name, 'selected': ''}

        filterSelected = request.GET.get('filter1', None)
        if filterSelected:
            filterSelected = int(filterSelected)
            if filterItems.get(filterSelected, None):
                filterItems[filterSelected]['selected'] = 'selected'

        return (filterItems, filterType)
