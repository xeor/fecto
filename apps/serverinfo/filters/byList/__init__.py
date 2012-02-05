
name = 'By list'

def filter(keys, dbObj):
    if not keys['filter_byList_value']:
        return False

    rawData = keys['filter_byList_value']
    servers = rawData.split()
    return dbObj.filter(name__in=servers)
