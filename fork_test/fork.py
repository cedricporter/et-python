#!/usr/bin/env python
import os, signal, sys, time, select, random
    
def child_make(i, read_end, write_end):
    fork_result = os.fork()
    if fork_result == 0:
        os.close(read_end)
        child_main(i, write_end)

def child_main(i, write_end):
    time.sleep(random.randint(30, 60))
    os.write(write_end, '=> %d' % i)
    print '[%d] end' % i
    sys.exit()

def make_pipe():
    read_end, write_end = os.pipe()
    return read_end, write_end

def main():
    read_fds = []
    for i in range(100):
        read_end, write_end = make_pipe()
        child_make(i, read_end, write_end)
        os.close(write_end)
        read_fds.append(read_end)

    while read_fds:
        rlist, wlist, xlist = select.select(read_fds, [], [])
        if len(rlist) != 0:
            for fd in rlist:
                read_fds.remove(fd)
                data = os.read(fd, 32)
                if not data: print 'empty'
                print data
            print len(read_fds)

    print 'parent died'

if __name__ == '__main__':
    #signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    main()
    

