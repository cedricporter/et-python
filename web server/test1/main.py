import socket

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 5555))
s.listen(10)

while True:
    client_fd, client_addr = s.accept()
    print client_addr, client_fd.recv(1024)
    client_fd.send('''HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\nETET\r\n\r\n''')
    client_fd.close()
