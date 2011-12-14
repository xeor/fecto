from django.contrib import admin
from django.conf.urls.defaults import patterns, url

from apps.siteconfig.models import Site, Text

class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')
    def has_add_permission(self, *args, **kwargs):    return False
    def has_delete_permission(self, *args, **kwargs): return False
    def has_change_permission(self, *args, **kwargs): return True
admin.site.register(Site, SiteAdmin)

class TextAdmin(admin.ModelAdmin):
    list_display = ('name', 'app', 'value', 'default', 'varType', 'permission', 'is_default')
    def has_add_permission(self, *args, **kwargs):    return False
    def has_delete_permission(self, *args, **kwargs): return False
    def has_change_permission(self, *args, **kwargs): return True
admin.site.register(Text, TextAdmin)
