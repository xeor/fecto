#!/usr/bin/env python

# TODO
#  Use fab instead!

# FIXMEs
# check pip
# check virtualenv command
# Generate random string in django
# Create virtualenv locally via script
# Use requirements.txt file with all needed packages, install in ext directory
# Run initial config script to create secret_key and such
# Set some permissions
# Run collectstatic
# Use activate_this.py when installing via pip?
# Info about redis install
# Info about config module and how to trigger.. Shall run automaticly
# Info about postgres install or another db
# mkdir -p static/CACHE/{css,js}
# mkdir ext
# Take apps/serverinfo/static/serverinfo/DataTables-1.8.1/ out of our git repo
#   https://github.com/DataTables/DataTables/tree/master/media
# Proxy option for pip..
#  pip --proxy=http://proxyserver:8080
#
# ./manage.py syncdb
# ./manage.py migrate
# ./manage.py collectstatic
# ./manage.py sync_config # TODO: change config (usedColumns) to newlineArray
# yum install redis
# ./manage.py migrate reversion

"""
activate_this = "/.../ext/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))
"""

import os, subprocess, sys

project_path = os.path.dirname(__file__) + '/..'

os.chdir(project_path)

def createConfFile(file, mapping):
    fp1 = open(file + '.template', 'r')
    fp2 = open(file, 'w')
    data = fp1.read()
    fp1.close()
    for key, value in mapping.items():
        data = data.replace(key, value)
    fp2.write(data)
    fp2.close()

def doVirtualEnv():
    if 'VIRTUAL_ENV' in os.environ:
        return os.environ['VIRTUAL_ENV']
    else:
        print 'Not inside virtualenv..'

    if not os.path.isdir('ext'):
        # Check if virtualenv exists
        print 'And it didnt exist. Trying to create.'
        os.mkdir('ext')
        subprocess.call(['virtualenv', 'ext'])

    print 'Rerun the setupscript after you have runned "source ext/bin/activate"'
    sys.exit(1)

virtualenv = doVirtualEnv()
print 'Will try to install all the requirements inside our virtualenv'
# This does not work as expected... :/
subprocess.call(['pip', 'install', '-E', virtualenv, '--requirement', os.path.join(project_path, 'setup/requirements.txt')])
