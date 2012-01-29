from django.conf import settings
import ipaddr

import reversion

from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.exceptions import ValidationError

#from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode

from apps.serverinfo.views import getAttributeTableHtml, getIpTableHtml
from apps.serverinfo.models import Server, IP, Vlan, AttributeMapping, AttributeValue, AttributeType, Note
from apps.serverinfo.helpers import server_columns

from lib.pinger import Pinger

class ServerInlineForm():
    def __init__(self):
        serverColumns = server_columns.ServerColumns()
        self.columnsDict = serverColumns.columnsDict

    def parseRequestedInlineFormData(self, request):
        serverObj = None
        requestSplit = request.split('.')

        if len(requestSplit) == 2:
            serverID = '.'.join(requestSplit[:-1])

        editable = [ i for i in self.columnsDict if self.columnsDict[i].get('editable', False) ]

        fielddata = requestSplit[-1]
        field = fielddata.split('-')[0]
        try:
            edittype = fielddata.split('-')[1]
        except:
            edittype = None

        if not field in editable:
            if edittype == 'attribute':
                serverObj = AttributeMapping.objects.get(id=field).server

        if not serverObj:
            serverObj = get_object_or_404(Server, id=serverID)

        return (serverObj, field, edittype)


    def getInlineFormData(self, keys):
        serverObj, field, edittype = self.parseRequestedInlineFormData(keys['id'])

        if field in ['virtual',]:
            current = str(getattr(serverObj, field))
            data = {'True': 'True', 'False': 'False', 'selected': current}

        if field in ['status',]:
            current = str(getattr(serverObj, field))
            data = dict(settings.APPS_SERVERINFO['status_levels'])

            # The entries in serverinfoConfig.statusLevels are django
            # ugettext objects for making translation possible. The
            # json encoder doesnt support this objects as default, so
            # we need to convert them to text now, before sending them
            # on to rest api for processing..
            for dataEntry in data:
                data[dataEntry] = force_unicode(data[dataEntry])

            data['selected'] = current

        return data

    def editInlineFormData(self, keys):
        value = keys.get('value', None)

        if value is None:
            raise Http404

        serverObj, field, edittype = self.parseRequestedInlineFormData(keys['id'])

        # Map common text to objects. We are getting them in plain/text from the request.
        mapping = {'True': True, 'False': False}
        if value in mapping:
            value = mapping[value]

        if edittype == 'attribute':
            attributeMappingObj = get_object_or_404(AttributeMapping, id=field)
            attributeValueObj = attributeMappingObj.attributeValue
            attributeValueObj.value = value
            attributeValueObj.save()
        else:
            setattr(serverObj, field, value)
            serverObj.save()

        return value

    def addAttribute(self, keys):
        value = keys.get('value', None)
        if value is None:
            raise Http404

        serverObj = get_object_or_404(Server, id=keys.get('server', None))
        attrTypeObj = get_object_or_404(AttributeType, id=keys.get('attrtype', None))

        attrValueObj = AttributeValue(value=value)
        attrValueObj.save()

        attrObj = AttributeMapping(attributeValue=attrValueObj, attributeType=attrTypeObj, server=serverObj)
        attrObj.save()

        rowHTML = getAttributeTableHtml(serverObj)
        value = {'row': rowHTML, 'multipleAllowed': attrTypeObj.multiple_allowed, 'id': attrTypeObj.id}
        return value

    def removeAttribute(self, keys):
        attrID = keys.get('id')
        attributeMappingObj = get_object_or_404(AttributeMapping, id=attrID)
        serverObj = attributeMappingObj.server
        attributeMappingObj.delete()

        rowHTML = getAttributeTableHtml(serverObj)

        value = {'row': rowHTML}

        return value

    def getFieldHistory(self, keys):
        """
        FIXME: work in progress.. just notes right now..
        NEXT
        """
        fieldID = keys.get('id')
        attributeMappingObj = get_object_or_404(AttributeMapping, id=attrID)
        serverObj = attributeMappingObj.server
        history = reversion.get_unique_for_object(serverObj)
        historyList = sorted([ (h.revision.date_created, h.field_dict) for h in history ])
        return historyList

    def addIP(self, keys):
        """

        """
        value = keys.get('value', None)
        if value is None:
            raise Http404

        serverObj = get_object_or_404(Server, id=keys.get('server', None))
        ipRaw = keys.get('value', None)

        if not ipRaw:
            print 'No id_value found'
            raise Http404

        try:
            ipObj = IP.objects.get(ip=ipRaw)
        except IP.DoesNotExist:
            ipObj = IP()
            ipObj.ip = ipRaw

            try:
                ipObj.save()
            except ValidationError:
                print 'Save failed'
                raise Http404

        serverObj.ip.add(ipObj)
        rowHTML = getIpTableHtml(serverObj)
        value = {'row': rowHTML}
        return value

    def checkIP(self, keys):
        # NEXT, IP verification stuff..
        #  Answers to ping?
        outputArray = []
        serverObj = get_object_or_404(Server, id=keys.get('server', None))
        ipRaw = keys.get('value', '')

        try:
            ipObj = ipaddr.IPv4Address(ipRaw)
            isValid = True
        except ipaddr.AddressValueError:
            isValid = False

        if isValid:
            outputArray.append('IP is valid')

            if Pinger().ping(ipRaw):
                outputArray.append('Is pingable')
            else:
                outputArray.append('Is not pingable')

            try:
                ipDbObj = IP.objects.get(ip=ipRaw)
            except IP.DoesNotExist:
                ipDbObj = None

            # VLan
            for i in Vlan.network_objects.all():
                subObj = ipaddr.IPv4Network(i.network)
                if ipObj in subObj:
                    outputArray.append('In VLan: %s' % unicode(i))
                    break

            # Used by other servers
            if ipDbObj and ipDbObj.server_set.count() >= 1:
                usedByTxt = ', '.join([ unicode(s) for s in ipDbObj.server_set.all() ])
                outputArray.append('Used by: %s.' % usedByTxt)

        else:
            outputArray.append('IP is invalid!')


        return {'status': ' -- '.join(outputArray)}

    def removeIP(self, keys):
        ipID = keys.get('id', '')
        serverID = keys.get('serverid', '')
        ipObj = get_object_or_404(IP, id=ipID)
        serverObj = get_object_or_404(Server, id=serverID)
        serverObj.ip.remove(ipObj)
        serverObj.save()

        rowHTML = getIpTableHtml(serverObj)

        value = {'row': rowHTML}

        return value

    def getNote(self, request):
        serverID = request.GET.get('serverid', None)
        serverObj = get_object_or_404(Server, id=serverID)

        noteType = request.GET.get('notetype', 'public')

        if request.user.is_authenticated():
            userObj = request.user
        else:
            userObj = None

        if noteType == 'private':
            if not userObj:
                return ''

            try:
                noteObj = Note.objects.get(server=serverObj, user=userObj, mode=2)
            except Note.DoesNotExist:
                return ''

            return {'note': noteObj.value, 'lastchange': noteObj.upd_time}

        if noteType == 'public':
            try:
                noteObj = Note.objects.get(server=serverObj, mode=1)
            except Note.DoesNotExist:
                return ''

            return {'note': noteObj.value, 'lastchange': noteObj.upd_time}

        return {'note': '', 'lastchange': 'never'}

    def setNote(self, request):
        serverID = request.POST.get('serverid', None)
        serverObj = get_object_or_404(Server, id=serverID)

        noteType = request.POST.get('notetype', 'public')
        noteContent = request.POST.get('note', '')

        print request.POST

        if request.user.is_authenticated():
            userObj = request.user
        else:
            userObj = None

        if noteType == 'private':
            if not userObj:
                return False

            try:
                noteObj = Note.objects.get(server=serverObj, user=userObj, mode=2)
                print 1
            except Note.DoesNotExist:
                print 2
                noteObj = Note(server=serverObj, user=userObj, mode=2)

            noteObj.value = noteContent
            noteObj.save()

            return True

        if noteType == 'public':
            try:
                noteObj = Note.objects.get(server=serverObj, mode=1)
            except Note.DoesNotExist:
                noteObj = Note(server=serverObj, mode=1)

            noteObj.user = userObj
            noteObj.value = noteContent
            noteObj.save()

            return True

        return False
