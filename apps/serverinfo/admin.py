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


class IPModelForm(forms.ModelForm):
    class Meta:
        model = IP

    def clean_ip(self):
        # We must find the correct subnet belonging to our ip, so we creates ipaddr objects first
        try:
            ip = self.cleaned_data['ip']
            ipObj = ipaddr.IPv4Address(ip)
        except:
            # Something failed, lets just pass the problem on, so the validators can take care of it :)
            return self.cleaned_data

        # Checks that our ip is indeed in a valid network
        for i in Vlan.network_objects.values():
            subObj = ipaddr.IPv4Network(i['network'])
            # We create a Vlan object based on the id from the vlans we are looping trough
            if ipObj in subObj:
                # And last, check if its already existing, and answering to ping.. If it is, deny, if override option is selected, allow
                # if ping(ip)...... FIXME
                return str(ipObj) # We need to convert the ip to a str before passing it on to our database..

        # If we get down here, we didnt find a subnet, and should return an error
        raise forms.ValidationError('IP doesnt belong to any of the registered vlans. You can add that here (FIXME, add link)')


class IPInline(admin.TabularInline):
    model = IP
    extra = 1
    form = IPModelForm

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
            #'/static/serverinfo/js/ipLocator.js',
            #'/media/js/jquery-1.3.2.min.js',
            #'/media/js/adminServer.js',
            #settings.ADMIN_MEDIA_PREFIX + "js/SelectBox.js",
            #settings.ADMIN_MEDIA_PREFIX + "js/SelectFilter2.js",
            )

class IPAdmin(admin.ModelAdmin):
    readonly_fields = ['vlan']
    list_display = ('ip', 'vlan')
    list_filter = ['vlan',]
    form = IPModelForm
    model = IP

    def save_model(self, request, obj, form, change):
        obj.fixVlan()

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
admin.site.register(IP, IPAdmin)

admin.site.register(AttributeType)
admin.site.register(AttributeValue)
admin.site.register(AttributeMapping)

admin.site.register(Note)
