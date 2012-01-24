import datetime
import ipaddr
import re
import pickle

from reversion.admin import VersionAdmin

from django.db.models.signals import post_save

from django.conf import settings
from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib.auth.models import User

from apps.siteconfig import conf
from apps.serverinfo import config
from apps.serverinfo.models import Vlan, Server, IP, AttributeType, \
    AttributeValue, AttributeMapping, Note


class ServerAdmin(VersionAdmin):
    list_display = ('name', 'function', 'description', 'reg_time', 'upd_time')
    list_filter = ['status']
    search_fields = ['name', 'function', 'description']
    readonly_fields = ['reg_time', 'upd_time']
    date_hierarchy = 'reg_time'
    #inlines = [IPInline,]
    ordering = ['-reg_time', ]

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.reg_time = datetime.datetime.now()
        obj.upd_time = datetime.datetime.today()
        obj.save()

    class Media:
        js = (
            #'/media/js/jquery-1.3.2.min.js',
            #'/media/js/adminServer.js',
            #settings.ADMIN_MEDIA_PREFIX + "js/SelectBox.js",
            #settings.ADMIN_MEDIA_PREFIX + "js/SelectFilter2.js",
            )

class VlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'network', 'vlanID', 'description')
    list_filter = ['location']
    search_fields = ['name', 'vlanID', 'description']

def saveVlanToIP(sender, **kwargs):
    obj = kwargs['instance']
    ipStr = kwargs['instance'].ip
    ipObj = ipaddr.IPv4Address(ipStr)
    if not obj.vlan:
        for i in Vlan.network_objects.values():
            subObj = ipaddr.IPv4Network(i['network'])
            if ipObj in subObj:
                # We creates a Vlan object based on the id from the vlans we are looping trough
                obj.vlan = Vlan.network_objects.get(id=i['id'])
                obj.save()
                break;
post_save.connect(saveVlanToIP, sender=IP)

admin.site.register(Server, ServerAdmin)
admin.site.register(Vlan, VlanAdmin)
admin.site.register(IP)

admin.site.register(AttributeType)
admin.site.register(AttributeValue)
admin.site.register(AttributeMapping)

admin.site.register(Note)
