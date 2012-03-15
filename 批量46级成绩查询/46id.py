# -*- coding:utf-8 -*-
# 从华工网上获取四六级准考证号
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
kssj:111
loginName:%C2%DE%BC%CE%B7%C9 (unable to decode value)
loginPass:200930635086
'''

def connect(username, userid):
    loginData = {'kssj':'111',
                'loginName':username.decode('utf-8').encode('gb2312'),
                'loginPass':userid}
    
    postData = urlencode(loginData)
    
    req = urllib2.Request('http://222.16.33.245:888/cetresult.asp', postData)
    cookieFile = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookieFile)  
    result = opener.open(req)    
    
    return re.findall(r'<td width="296">(\d{15})</td>', result.read())
    

def GetScore(id, username):
    loginData = {'id':id,
                'name':username.decode("utf-8").encode("gbk")
                }
    
    
    
    postData = urlencode(loginData)
    
    print postData
    
    req = urllib2.Request('http://cet.99sushe.com/s')
    req.add_header("Origin", "http://cet.99sushe.com")
    req.add_header("Referer", "http://cet.99sushe.com")
    req.add_data(postData)
    cookieFile = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookieFile)  
    result = opener.open(req)    
    
    return result.read()


def main():
    file = open('user.txt')
    file2 = open('id.txt', 'w')
    
    userinfo = []
    
    for line in file:
        id, name = line.split()[0], line.split()[1]
        userinfo.append((id, name))   
        
    id_nameList = []     
        
    for id, name in userinfo:
        try:
            eid = connect(name, id)[ 0 ]
            print eid,
            print name
            file2.write(eid + ' ')
            file2.write(name)
            file2.write('\n')
            #id_nameList.append((eid, name))
            #print GetScore(id, name)
        except:
            pass
        
    file2.close()
        
    for id, name in id_nameList:
        print id,
        print name
        #GetScore(id, name)
        
    
        

if __name__ == '__main__':
    main()


