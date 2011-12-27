from apps.serverinfo import config as serverinfoConfig

def status(value):
    if value == '6': # hidden
        appendedText = '<span class="red">(CHANGEME!)</span>'
    else:
        appendedText = ''

    statusText = serverinfoConfig.statusLevelsDict[value]

    return '%s %s' % (statusText, appendedText)
