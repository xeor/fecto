from django.utils.encoding import force_unicode

from apps.serverinfo import config as serverinfoConfig

def status(value):
    if value == '6': # hidden
        appendedText = '<span class="red">(CHANGEME!)</span>'
    else:
        appendedText = ''

    statusText = force_unicode(dict(serverinfoConfig.statusLevels)[value])

    return '%s %s' % (statusText, appendedText)
