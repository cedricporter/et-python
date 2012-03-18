#!/usr/bin/env python
# author:  Hua Liang [ Stupid ET ]
# email:   et@everet.org
# website: http://EverET.org
#
import socket, os, stat, threading, time


class FTPConnection:
    '''You can add handle func by startswith handle_ prefix.
    When the connection receives CWD command, it'll use handle_CWD to handle it.
    '''
    def __init__(self, fd, remote_ip):
        self.fd = fd
        self.data_fd = 0
        self.data_host = ''
        self.data_port = 0
        self.curr_dir = 'd:/'
        self.running = True
        self.handler = dict(
            [(method[7:], getattr(self, method)) \
            for method in dir(self) \
            if method.startswith("handle_") and callable(getattr(self, method))])

    def start(self):
        self.say_welcome()

        try:
            while self.running:
                success, command, arg = self.recv()
                print '[', command, ']', arg
                if not success: 
                    self.send_msg(500, "Failed")
                    continue
                if not self.handler.has_key(command):
                    self.send_msg(500, "Command Not Found")
                    continue
                self.handler[command](arg)
        except:
            return False

        self.say_bye()
        return True

    def send_msg(self, code, msg):
        message = str(code) + ' ' + msg + '\r\n'
        self.fd.send(message)

    def recv(self):
        '''returns 3 tuples, success, command, arg'''
        try:
            success, buf, command, arg = True, '', '', ''
            while True:
                buf += self.fd.recv(4096)
                if buf[-2:] == '\r\n': break
            split = buf.find(' ')
            command, arg = (buf[:split], buf[split + 1:].strip()) if split != -1 else (buf.strip(), '')
        except:
            success = False

        return success, command, arg


    def say_welcome(self):
        self.send_msg(220, "Welcome to EverET.org FTP")

    def say_bye(self):
        self.send_msg(220, "Good Bye")

    def connect(self):
        '''establish data connection'''
        if self.data_fd == 0:
            self.send_msg(500, "no data connection")
            return False
        else:
            try:
                self.data_fd.connect((self.data_host, self.data_port))
            except:
                self.send_msg(500, "failed to connect")
                return False
        return True

    def close_data_fd(self):
        self.data_fd.close()
        self.data_fd = 0

    # Command Handlers
    def handle_USER(self, arg):
        self.send_msg(230, "OK")
    def handle_PASS(self, arg):
        self.send_msg(230, "OK")
    def handle_QUIT(self, arg):
        self.handle_BYE()
    def handle_BYE(self, arg):
        self.running = False
        self.send_msg(200, "OK")
    def handle_CDUP(self, arg):
        self.curr_dir = self.curr_dir[:self.curr_dir.rfind('/')]
        self.send_msg(200, "OK")
    def handle_PWD(self, arg):
        self.send_msg(257, self.curr_dir)
    def handle_CWD(self, arg):
        self.curr_dir += '/' + arg
        self.send_msg(250, "OK")
    def handle_SYST(self, arg):
        self.send_msg(215, "UNIX")
    def handle_TYPE(self, arg):
        self.send_msg(220, "OK")
    def handle_LIST(self, arg):
        if not self.connect(): return 
        self.send_msg(125, "OK")
        template = "%s%s%s------- %04u %8s %8s %8lu %s %s\r\n"
        for filename in os.listdir(self.curr_dir):
            path = self.curr_dir + '/' + filename
            status = os.stat(path)
            self.data_fd.send(template % (
                'd' if os.path.isdir(path) else '-',
                'r',
                'w', 
                1, '0', '0', 
                status[stat.ST_SIZE], 
                time.strftime("%b %d  %Y", time.localtime(status[stat.ST_MTIME])), 
                filename))
        self.send_msg(226, "Limit")
        self.close_data_fd()
    def handle_PORT(self, arg):
        try:
            if self.data_fd:
                self.data_fd.close()
            t = arg.split(',')
            self.data_host = '.'.join(t[:4])
            self.data_port = int(t[4]) * 256 + int(t[5])
            self.data_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print self.data_host, self.data_port
        except:
            self.send_msg(500, "PORT failed")
        self.send_msg(200, "OK")


class FTPThread(threading.Thread):
    '''FTPConnection Thread Wrapper'''
    def __init__(self, fd, remote_ip):
        threading.Thread.__init__(self)
        self.ftp = FTPConnection(fd, remote_ip)

    def run(self):
        self.ftp.start()


class FTPServer:
    def serve_forever(self):
        host = '0.0.0.0'
        port = 21
        s = socket.socket()
        s.bind((host, port))
        s.listen(512)
        while True:
            client_fd, client_addr = s.accept()
            handler = FTPThread(client_fd, client_addr)
            handler.start()

def main():
    server = FTPServer()
    server.serve_forever()

if __name__ == '__main__':
    main()
