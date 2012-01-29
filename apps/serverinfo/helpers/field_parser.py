from apps.serverinfo import config as serverinfoConfig
from apps.serverinfo.helpers import server_columns

serverColumns = server_columns.ServerColumns()

def status(value):
    if value == '6': # hidden
        appendedText = '<span class="red">(CHANGEME!)</span>'
    else:
        appendedText = ''

    statusText = serverColumns.statusLevelsDict[value]

    return '%s %s' % (statusText, appendedText)
