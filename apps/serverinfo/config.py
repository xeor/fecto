# FIXME, handle separators in serverlist
# FIXME, move all this columns stuff out of config.py!

filters = [
    {'name': 'VLan/subnet', 'id': 'subnet'},
    {'name': 'Manual', 'id': 'manual',},
    ]

# Configuration which are dynamicly gathered and made available in the
# admin, DONT change this without knowing what you are doing.. Its
# internally used. Not in use yet :)
Text = {
    'site': {'description': 'some description', 'default': 'default', 'permission': 'some permission'},
    'site2': {'description': 'some description4', 'default': 'some default4',},
    'site3': {'description': 'some description', 'default': 'some default1',},
    'site4': {'description': 'some description2', 'default': 'some default',},
    }
