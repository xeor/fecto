"""
Original from https://code.djangoproject.com/wiki/SplitSettings#SettingInheritancewithHierarchy
but modified to fit the Fecto project
"""

import os
import pkgutil

import apps

# certain keys we want to merge instead of copy
merge_keys = ('INSTALLED_APPS', 'MIDDLEWARE_CLASSES')

def deep_update(from_dict, to_dict):
    for (key, value) in from_dict.iteritems():
        if key in to_dict.keys() and isinstance(to_dict[key], dict) and isinstance(value, dict):
            deep_update(value, to_dict[key])
        elif key in merge_keys:
            if not key in to_dict:
                to_dict[key] = ()
            to_dict[key] = to_dict[key] + from_dict[key]
        else:
            to_dict[key] = value

# this should be one of prod, dev. Default to dev for safety.
env = os.environ.get('APP_ENV', 'dev')

appPath = os.path.dirname(apps.__file__)
appNames = tuple(['apps.' + name + '.settings' for modLoader, name, isPkg in pkgutil.iter_modules([appPath])])

modules = ('upstream', 'common', env) + appNames

current = __name__
for module_name in modules:
    try:
        print 'Loading', module_name
        module = getattr(__import__(current, globals(), locals(), [module_name]), module_name)
    except ImportError, e:
        print 'ERROR: Unable to import %s configuration because of ImportError: %s' % (module_name, e)
        raise
    except AttributeError, e:
        if env == 'dev':
            print 'WARNING: Unable to import %s because of AttributeError: %s' % (module_name, e)
        else:
            raise

    # create a local copy of this module's settings
    module_settings = {}
    for setting in dir(module):
        # all django settings are uppercase, so this ensures we
        # are only processing settings from the dir() call
        if setting == setting.upper():
            module_settings[setting] = getattr(module, setting)
    deep_update(module_settings, locals())

#print locals() # for debugging