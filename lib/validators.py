from django.core.exceptions import ValidationError
from ipaddr import IPv4Network
import re

def isValidIPv4Network(network):
    try:
        if not re.search(r'^[0-9\.]+/[0-9]+$', network):
            raise Exception()
        subnet = IPv4Network(network)
        return True
    except Exception:
        raise ValidationError('Invalid format, use eg. "127.0.0.1/8"')
