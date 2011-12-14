#!/usr/bin/env python

def filter(input, dbObj):
    # FIXME, not done at all!

    return dbObj.filter(name__icontains=input['value'])
