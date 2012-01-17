import ipaddr

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User

from apps.contact.models import Location

from apps.serverinfo.config import statusLevels

from lib.fields import IPNetworkQuerySet
from lib.validators import isValidIPv4Network

class Vlan(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    network = models.CharField(max_length=18, validators=[isValidIPv4Network], db_index=True)
    network_objects = IPNetworkQuerySet.as_manager()
    vlanID = models.IntegerField(blank=True, null=True, db_index=True)
    location = models.ForeignKey(Location, blank=True, null=True, db_index=True)
    skipFirst = models.IntegerField(blank=True, null=True, help_text=_('Dont use the first X IP\'s when calculating the next ip.'))
    skipEnd = models.IntegerField(blank=True, null=True, help_text=_('Dont use the last X IP\'s when calculating the next ip.'))
    description = models.TextField(blank=True, null=True, db_index=True)

    def __unicode__(self):
        try:
            return self.location.name + ' (' + self.name + ')'
        except:
            return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'VLan\'s'

    def getNextAvailableIP(self):
        subnetObj = ipaddr.IPv4Network(self.network)

        # All used ips is stored in this list
        allIPs = []
        [ allIPs.append(ipaddr.IPv4Address(i.ip)) for i in IP.objects.filter(vlan=self) ]

        if self.skipFirst:
            skipFirst = int(self.skipFirst)
        else:
            # Skip the first 10 as default.. FIXME, configurable
            skipFirst = 10

        if self.skipEnd:
            skipEnd = int(self.skipEnd)
        else:
            # Dont reserve end ips as default.. FIXME, configurable
            skipEnd = 0

        lastTry = subnetObj.numhosts - skipEnd - 1 # Very last one is broadcast
        counter = 0
        for i in subnetObj.iterhosts():
            counter += 1
            if counter <= skipFirst:
                continue

            if counter >= lastTry:
                return 'None left'

            if i not in allIPs:
                return i

        return 'Error..'

class IP(models.Model):
    ip = models.IPAddressField(unique=True)
    vlan = models.ForeignKey(Vlan, blank=True, null=True) # Autopopulated field

    def __unicode__(self):
        return self.ip
        #return u'%s (%s)' % (self.ip, self.vlan)

    class Meta:
        ordering = ['vlan', 'ip']
        verbose_name_plural = 'IP\'s'

    def fixVlan(self):
        ipObj = ipaddr.IPv4Address(self.ip)
        for i in Vlan.network_objects.all():
            subObj = ipaddr.IPv4Network(i.network)
            if ipObj in subObj:
                self.vlan = i
                self.save()
                break

    def getGateway(self):
        # Returns firs ip in the network..
        if self.vlan:
            ipObj = ipaddr.IPv4Network(self.vlan.network)
            return ipObj.iterhosts().next()
        return _('(No gateway)')

    def getSubnet(self): # was 'subnet'
        if self.vlan:
            ipObj = ipaddr.IPv4Network(self.vlan.network)
            return ipObj.netmask.exploded
        return _('(No subnet)')

    def getShared(self):
        return Server.objects.filter(ip=self)

def checkIP(sender, **kwargs):
    obj = kwargs['instance']
    ipStr = kwargs['instance'].ip
    try:
        ipObj = ipaddr.IPv4Address(ipStr)
    except ipaddr.AddressValueError:
        raise ValidationError('Invalid IPv4 address.')
pre_save.connect(checkIP, sender=IP)

def fixVlan(sender, **kwargs):
    obj = kwargs['instance']
    if not obj.vlan:
        obj.fixVlan()
post_save.connect(fixVlan, sender=IP)



class Server(models.Model):
    # Remember add new options to config.py as well.. All the configuration is there..

    name = models.CharField(max_length=64, unique=True, db_index=True)
    function = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    description = models.TextField(blank=True, null=True, db_index=True)
    note = models.TextField(blank=True, null=True, help_text=_('IT note field. Not server description! Use only for temporary notes'))
    #virtual = models.BooleanField(default=True) # Attribute
    ip = models.ManyToManyField(IP, blank=True, null=True)
    status = models.CharField('Status', blank=True, null=True, max_length=1, choices=statusLevels, default=2)

    reg_time = models.DateTimeField('Registered', blank=True, null=True, auto_now_add=True)
    upd_time = models.DateTimeField('Updated', blank=True, null=True, auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

    #def ip_list(self): return ', '.join([ i.ip for i in self.ip_server_related.all() ])

    def actions(self):
        # FIXME, dynamic
        actions = []
        #actions.append('<a href="http://' + self.name + '-ilo">iLO</a>')
        actions.append('<a href="rdp://' + self.name + '">RDP</a>')
        actions.append('<a href="ssh://' + self.name + '">SSH</a>')
        return actions


class AttributeType(models.Model):
    id_name = models.CharField(max_length=32, db_index=True, unique=True)
    name = models.CharField(max_length=32, db_index=True)
    autopopulated = models.BooleanField(default=False) # Means they cant be edited, FIXME
    description = models.TextField(blank=True, null=True, db_index=True)
    multiple_allowed = models.BooleanField(default=True, db_index=True) # FIXME, verifier
    # FIXME
    # look for name + '_validator', '_to_python', '_from_python', '_html' and
    # so on functions.. Maybe use some stuff from django newforms?

    # FIXME
    # Check that the name is not in the reserved internal used column names

    def __unicode__(self):
        return self.name

class AttributeValue(models.Model): # Server attributes
    value = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True, db_index=True)
    # FIXME: pickled field..

    def __unicode__(self):
        return self.value

class AttributeMapping(models.Model):
    attributeValue = models.ForeignKey(AttributeValue)
    attributeType = models.ForeignKey(AttributeType)
    server = models.ForeignKey(Server)

    def __unicode__(self):
        return '%s - %s - %s' % (self.server.name, self.attributeType.name, self.attributeValue.value)

class Note(models.Model):
    server = models.ForeignKey(Server, db_index=True, related_name='note_server_related')
    user = models.ForeignKey(User, blank=True, null=True, db_index=True)
    mode = models.CharField(max_length=1, default=1, db_index=True) # 1=public, 2=private
    upd_time = models.DateTimeField(auto_now=True)
    value = models.TextField()

    def __unicode__(self):
        return '%s - %s' % (self.server.name, self.value,)
