#!/usr/bin/env python

import socket, pprint

solist = [x for x in dir(socket) if x.startswith('SO_')]
solist.sort()
pprint.pprint(solist)

