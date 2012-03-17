import socket

s = socket.socket()

host = '192.168.1.111'
port = 1990
port = 9877

s.connect((host, port))

while True:
    sendline = raw_input()
    s.send(sendline)
    print s.recv(1024)

print s.recv(1024)
