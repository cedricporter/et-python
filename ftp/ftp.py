#!/usr/bin/env python
# author:  Hua Liang [ Stupid ET ]
# email:   et@everet.org
# website: http://EverET.org
#
import socket, os, stat, threading, time, sys, re

host = '0.0.0.0'
port = 21

runas_user = 'www-data'

account_info = {
    'et':{'pass':'12345', 'home_dir':'/root/'},
    'lst':{'pass':'54321', 'home_dir':'/tmp/'}
    }

class FTPConnection:
    '''You can add handle func by startswith handle_ prefix.
    When the connection receives CWD command, it'll use handle_CWD to handle it.
    '''
    def __init__(self, fd, remote_ip):
        self.fd = fd
        self.data_fd = 0
        self.options = {'pasv': False, 'utf8': False}
        self.data_host = ''
        self.data_port = 0
        self.localhost = fd.getsockname()[0]
        self.home_dir = '/tmp/'
        self.curr_dir = '/'
        self.running = True
        self.handler = dict(
            [(method[7:], getattr(self, method)) \
            for method in dir(self) \
            if method.startswith("handle_") and callable(getattr(self, method))])

    def start(self): 
        try:
            self.say_welcome()
            while self.running:
                success, command, arg = self.recv()
                command = command.upper()
                if self.options['utf8']:
                    arg = unicode(arg, 'utf8').encode(sys.getfilesystemencoding())
                print '[', command, ']', arg
                if not success: 
                    self.send_msg(500, "Failed")
                    continue
                if not self.handler.has_key(command):
                    self.send_msg(500, "Command Not Found")
                    continue
                self.handler[command](arg)
            self.say_bye()
            self.client_fd.close()
        except Exception, e:
            self.running = False
            print e

        return True

    def send_msg(self, code, msg):
        if self.options['utf8']:
            msg = unicode(msg, sys.getfilesystemencoding()).encode('utf8')
        message = str(code) + ' ' + msg + '\r\n'
        self.fd.send(message)

    def recv(self):
        '''returns 3 tuples, success, command, arg'''
        try:
            success, buf, command, arg = True, '', '', ''
            while True:
                data = self.fd.recv(4096)
                if not data:
                    self.running = False
                    break
                buf += data
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
        if path[0] != '/': path = self.curr_dir + '/' + path
        print 'parse_path', path
        split_path = os.path.normpath(path).replace('\\', '/').split('/')
        remote = '' 
        local = self.home_dir
        print split_path
        for item in split_path:
            if item.startswith('..') or item == '': continue # ignore parent directory
            remote += '/' + item
            local += '/' + item
        if remote == '': remote = '/'
        print 'remote', remote, 'local', local
        return remote, local

    # Command Handlers
    def handle_USER(self, arg):
        if arg in account_info:
            self.username = arg
            self.send_msg(331, "Need password")
        else:
            self.send_msg(500, "Invalid User")
            self.running = False
    def handle_PASS(self, arg):
        if arg == account_info[self.username]['pass']: 
            self.home_dir = account_info[self.username]['home_dir']
            self.send_msg(230, "OK")
        else:
            self.send_msg(500, "Invalid Password")
            self.running = False
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
    def handle_XPWD(self, arg):
        self.handle_PWD(arg)
    def handle_PWD(self, arg):
        print 'in PWD', self.curr_dir
        remote, local = self.parse_path(self.curr_dir)
        self.send_msg(257, '"' + remote + '"')
    def handle_CWD(self, arg):
        remote, local = self.parse_path(arg)
        if not os.path.exists(local):
            self.send_msg(500, "Path not exist")
            return
        print 'handle_CWD', remote
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
        if os.path.exists(local):
            self.send_msg(500, "Folder is already existed")
            return
        os.mkdir(local)
        self.send_msg(257, "OK")
    def handle_XRMD(self, arg):
        self.handle_RMD(arg)
    def handle_RMD(self, arg):
        remote, local = self.parse_path(arg)
        if not os.path.exists(local):
            self.send_msg(500, "Folder is not existed")
            return
        os.rmdir(local)
        self.send_msg(250, "OK")
    def handle_LIST(self, arg):
        if not self.data_connect(): return 
        self.send_msg(125, "OK")
        template = "%s%s%s------- %04u %8s %8s %8lu %s %s\r\n"
        remote, local = self.parse_path(self.curr_dir)
        for filename in os.listdir(local):
            path = local + '/' + filename
            if os.path.isfile(path) or os.path.isdir(path): # ignores link or block file
                status = os.stat(path)
                msg = template % (
                    'd' if os.path.isdir(path) else '-',
                    'r', 'w', 1, '0', '0', 
                    status[stat.ST_SIZE], 
                    time.strftime("%b %d  %Y", time.localtime(status[stat.ST_MTIME])), 
                    filename)
                if self.options['utf8']: msg = unicode(msg, sys.getfilesystemencoding()).encode('utf8')
                self.data_fd.send(msg)
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
    def handle_DELE(self, arg):
        remote, local = self.parse_path(arg)
        if not os.path.exists(local):
            self.send_msg(450, "File not exist")
            return
        os.remove(local)
        self.send_msg(250, 'File deleted')
    def handle_OPTS(self, arg):
        print 'in OPTS'
        if arg.upper() == "UTF8 ON":
            self.options['utf8'] = True
            self.send_msg(200, "OK")
        elif arg.upper() == "UTF8 OFF":
            self.options['utf8'] = False
            self.send_msg(200, "OK")
        else:
            self.send_msg(500, "Invalid argument")
            


class FTPThread(threading.Thread):
    '''FTPConnection Thread Wrapper'''
    def __init__(self, fd, remote_ip):
        threading.Thread.__init__(self)
        self.ftp = FTPConnection(fd, remote_ip)

    def run(self):
        self.ftp.start()
        print "Thread done"

class FTPThreadServer:
    '''FTP Server which is using thread'''
    def serve_forever(self):
        s = socket.socket()
        s.bind((host, port))
        s.listen(512)
        while True:
            print 'new server'
            client_fd, client_addr = s.accept()
            handler = FTPThread(client_fd, client_addr)
            handler.start()

class FTPForkServer:
    '''FTP Fork Server, use process per user'''
    def serve_forever(self):
        s = socket.socket()
        s.bind((host, port))
        s.listen(512)
        while True:
            print 'new server'
            client_fd, client_addr = s.accept()
            #try:
            fork_result = os.fork()
            if fork_result == 0: # child process
                uid = get_uid(runas_user)
                os.setuid(uid)
                os.setgid(uid)
                print uid
                handler = FTPConnection(client_fd, client_addr)
                handler.start()
                break
            #except:
            #    print 'Fork failed'

def get_uid(username = 'www-data'):
    '''get uid by username, I don't know whether there's a
    function can get it, so I wrote this function.'''
    pwd = open('/etc/passwd', 'r')
    pat = re.compile(username + ':.*?:(.*?):.*?')
    for line in pwd.readlines():
        try:
            uid = pat.search(line).group(1)
        except: continue
        return int(uid)


def main():
    #server = FTPThreadServer()
    server = FTPForkServer()
    server.serve_forever()

if __name__ == '__main__':
    import sys
    #sys.stdout = open('/var/log/ftp.py.log', 'w')
    main()
