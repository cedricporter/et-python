#!/usr/bin/env python

import socket, pprint, traceback, sys

solist = [x for x in dir(socket) if x.startswith('SO_')]
solist.sort()
pprint.pprint(solist)

def func():
        1 / 0

try:
    func()
except:
    traceback.print_exc()
    print
    print sys.exc_info()

    
