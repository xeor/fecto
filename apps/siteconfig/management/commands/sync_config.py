import sys

from django.conf import settings

from django.core.management.base import BaseCommand
from apps.siteconfig.conf import Conf

class Command(BaseCommand):
    args = ''
    help = 'Crawl apps and add configs options'
    configTypes = ('Text', 'm2m')

    def handle(self, *args, **options):
        c = Conf()

        for app in settings.INSTALLED_APPS:
            if not app.startswith('apps.'): # Not one of our local apps
                continue

            configObjName = '%s%s' % (app,'.config')
            try:
                __import__(configObjName) # To get it into sys.modules
            except ImportError:
                continue
            configObj = sys.modules[configObjName]

            for configType in self.configTypes:
                if hasattr(configObj, configType):
                    configDict = getattr(configObj, configType)
                    for name in configDict:
                        item = configDict[name]
                        default = item.get('default', None)
                        permission = item.get('permission', None)
                        description = item.get('description', None)
                        if c.add(configType, name, app, default, permission, description):
                            self.stdout.write('Added "%s" with type "%s" in app "%s"\n' % (name, configType, app))
                        else:
                            self.stdout.write('Skipping (already there) "%s" in app "%s"' % (name, app))
                            updatedInfo = c.updateInfo(configType, name, app, default, description)
                            if updatedInfo:
                                self.stdout.write(' - updated info for %s' % (', '.join(updatedInfo),))
                            self.stdout.write('\n')
