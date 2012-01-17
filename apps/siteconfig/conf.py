from django.core.cache import cache

from apps.siteconfig import models

# FIXME
#  - Make sure it caches the config for a long time! Refresh the cache manually if it changes, TEST

class Conf:
    def _getDbObj(self, confType, name, app):
        if not hasattr(models, confType):
            return False

        dbObj = getattr(models, confType)

        try:
            return dbObj.objects.get(name=name, app=app)
        except dbObj.DoesNotExist:
            dbObj = dbObj(name=name, app=app)
            dbObj.save()
            return dbObj


    def add(self, confType, name, appName = '', default = '', permissions = '', description = ''):
        dbObj = self._getDbObj(confType, name, appName)
        dbObj.app = appName
        dbObj.name = name
        dbObj.value = default
        dbObj.default = default
        dbObj.permission = permissions
        dbObj.description = description
        dbObj.varType = confType
        dbObj.save()
        return True

    def get(self, confType, name, app):
        value = cache.get('conf_%s_%s' % (app, name), None)
        if not value:
            dbObj = self._getDbObj(confType, name, app)

            varType = dbObj.varType

            if varType == 'Text':
                value = dbObj.value.strip()
            if varType == 'newlineArray':
                value = dbObj.value.split('\n')
                value = [ x.strip() for x in value ]

            cache.set('%s_%s' % (app, name), value, 60*60*24)

        return value

    def updateInfo(self, confType, name, appName = None, default = None, description = None):
        dbObj = self._getDbObj(confType, name, appName)

        changes = []

        if (default) and (dbObj.default != default):
            dbObj.default = default
            changes.append('default')

        if (description) and (dbObj.description != description):
            dbObj.description = description
            changes.append('description')

        if changes:
            dbObj.save()
            return changes
        else:
            return False
