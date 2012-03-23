#!/usr/bin/env python
import sys, socket, time, threading

loglock = threading.Lock()
def log(msg):
    loglock.acquire()
    try:
        print '[%s]: \n%s\n' % (time.ctime(), msg.strip())
        sys.stdout.flush()
    finally:
        loglock.release()

class PipeThread(threading.Thread):
    def __init__(self, source, target):
        threading.Thread.__init__(self)
        self.source = source
        self.target = target

    def run(self):
        while True:
            try:
                data = self.source.recv(1024)
                log(data)
                if not data: break
                self.target.send(data)
            except:
                break
        log('PipeThread done')

class Forwarding(threading.Thread):
    def __init__(self, port, targethost, targetport):
        threading.Thread.__init__(self)
        self.targethost = targethost
        self.targetport = targetport
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0', port))
        self.sock.listen(10)
    def run(self):
        while True:
            client_fd, client_addr = self.sock.accept()
            target_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_fd.connect((self.targethost, self.targetport))
            log('new connect')
            # two direct pipe
            PipeThread(target_fd, client_fd).start()
            PipeThread(client_fd, target_fd).start()
            

if __name__ == '__main__':
    print 'Starting'
    import sys
    try:
        port = int(sys.argv[1])
        targethost = sys.argv[2]
        try: targetport = int(sys.argv[3])
        except IndexError: targetport = port
    except (ValueError, IndexError):
        print 'Usage: %s port targethost [targetport]' % sys.argv[0]
        sys.exit(1)

    #sys.stdout = open('forwaring.log', 'w')
    Forwarding(port, targethost, targetport).start()
          
