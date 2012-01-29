INSTALLED_APPS = (
    'apps.serverinfo',
)

# Since we might be changing the list we are getting out from APPS_SERVERINFO, remember to make a copy of it first!
# Example, use, visibleColumns = list(settings.APPS_SERVERINFO['visible_columns'])! list() makes a new copy, not
# just a reference to the object. If you make a reference and change it, funny things can happen..
APPS_SERVERINFO = {
    'visible_columns': [
        # What columns from the default datafields should be visible? You can also change the order of appearance.
        u'name',
        u'function',
        u'description',
        u'note',
        u'ip',
        u'status',
        u'reg_time',
        u'upd_time',
        u'actions',
    ],
}