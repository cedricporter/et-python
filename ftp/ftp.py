#!/usr/bin/env python
# author:  Hua Liang [ Stupid ET ]
# email:   et@everet.org
# website: http://EverET.org
#
import socket, os, stat, threading, time

listen_host = '0.0.0.0'

class FTPConnection:
    '''You can add handle func by startswith handle_ prefix.
    When the connection receives CWD command, it'll use handle_CWD to handle it.
    '''
    def __init__(self, fd, remote_ip):
        self.fd = fd
        self.data_fd = 0
        self.options = {'pasv': False}
        self.data_host = ''
        self.data_port = 0
        self.localhost = fd.getsockname()[0]
        self.home_dir = os.path.normpath(os.path.abspath(os.curdir)).replace('\\', '/')
        self.curr_dir = '/'
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
        except Exception, e:
            self.running = False
            print e

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
        self.handle_BYE('')

    def data_connect(self):
        '''establish data connection'''
        if self.data_fd == 0:
            self.send_msg(500, "no data connection")
            return False
        elif self.options['pasv']:
            fd, addr = self.data_fd.accept()
            self.data_fd.close()
            self.data_fd = fd
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

    def parse_path(self, path):
        if path == '': path = '.'
        if path[0] != '/':
            path = self.curr_dir + '/' + path
        print 'parse_path', path
        split_path = os.path.normpath(path).replace('\\', '/').split('/')
        remote = ''
        local = self.home_dir
        for item in split_path:
            item = item.lstrip('.')
            if item == '': continue
            remote += '/' + item
            local += '/' + item
        if remote == '': remote = '/'
        print 'remote', remote, 'local', local
        return remote, local

    # Command Handlers
    def handle_USER(self, arg):
        self.send_msg(230, "OK")
    def handle_PASS(self, arg):
        self.send_msg(230, "OK")
    def handle_QUIT(self, arg):
        self.handle_BYE(arg)
    def handle_BYE(self, arg):
        self.running = False
        self.send_msg(200, "OK")
    def handle_CDUP(self, arg):
        self.send_msg(500, 'failed')
        return
        self.curr_dir = self.curr_dir[:self.curr_dir.rfind('/')]
        self.send_msg(200, "OK")
    def handle_PWD(self, arg):
        print 'in PWD', self.curr_dir
        remote, local = self.parse_path(self.curr_dir)
        self.send_msg(257, remote)
    def handle_CWD(self, arg):
        remote, local = self.parse_path(arg)
        self.curr_dir = remote
        self.send_msg(250, "OK")
    def handle_SIZE(self, arg):
        remote, local = self.parse_path(self.curr_dir)
        self.send_msg(231, str(os.path.getsize(local)))
    def handle_SYST(self, arg):
        self.send_msg(215, "UNIX")
    def handle_STOR(self, arg):
        print 'in STOR'
        remote, local = self.parse_path(arg)
        if not self.data_connect(): return
        self.send_msg(125, "OK")
        f = open(local, 'wb')
        print f, local
        while True:
            data = self.data_fd.recv(8192)
            if len(data) == 0: break
            f.write(data)
        f.close()
        self.close_data_fd()
        self.send_msg(226, "OK")
    def handle_RETR(self, arg):
        print 'in RETR'
        remote, local = self.parse_path(arg)
        if not self.data_connect(): return
        self.send_msg(125, "OK")
        f = open(local, 'rb')
        print f, local
        while True:
            data = f.read(8192)
            if len(data) == 0: break
            self.data_fd.send(data)
        f.close()
        self.close_data_fd()
        self.send_msg(226, "OK")
    def handle_TYPE(self, arg):
        self.send_msg(220, "OK")
    def handle_RNFR(self, arg):
        remote, local = self.parse_path(arg)
        self.rename_tmp_path = local
        self.send_msg(350, 'rename from ' + remote)
    def handle_RNTO(self, arg):
        remote, local = self.parse_path(arg)
        os.rename(self.rename_tmp_path, local)
        self.send_msg(250, 'rename to ' + remote)
    def handle_NLST(self, arg):
        if not self.data_connect(): return
        self.send_msg(125, "OK")
        remote, local = self.parse_path(self.curr_dir)
        for filename in os.listdir(local):
            self.data_fd.send(filename + '\r\n')
        self.send_msg(226, "Limit")
        self.close_data_fd()
    def handle_XMKD(self, arg):
        self.handle_MKD(arg)
    def handle_MKD(self, arg):
        remote, local = self.parse_path(arg)
        os.mkdir(local)
        self.send_msg(257, "OK")
    def handle_XRMD(self, arg):
        self.handle_RMD(arg)
    def handle_RMD(self, arg):
        remote, local = self.parse_path(arg)
        os.rmdir(local)
        self.send_msg(250, "OK")
    def handle_LIST(self, arg):
        if not self.data_connect(): return 
        self.send_msg(125, "OK")
        template = "%s%s%s------- %04u %8s %8s %8lu %s %s\r\n"
        remote, local = self.parse_path(self.curr_dir)
        for filename in os.listdir(local):
            path = local + '/' + filename
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
    def handle_PASV(self, arg):
        self.options['pasv'] = True
        try:
            self.data_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.data_fd.bind((self.localhost, 0))
            self.data_fd.listen(1)
            ip, port = self.data_fd.getsockname()
            self.send_msg(227, 'Enter Passive Mode (%s,%u,%u).' %
                    (','.join(ip.split('.')), (port >> 8 & 0xff), (port & 0xff)))
        except Exception, e:
            print e
            self.send_msg(500, 'passive mode failed')
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
        host = listen_host
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
