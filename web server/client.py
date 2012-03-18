import socket

host = '192.168.1.111'
port = 1990

s = socket.socket()
s.connect((host, port))

while True:
    sendline = raw_input()
    s.send(sendline)
    print s.recv(1024)
