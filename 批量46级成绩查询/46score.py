# -*- coding:utf-8 -*-
# 从99sushe获取四六级成绩
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

'''
您的成绩总分：387
听力：144
阅读：140
综合：39
写作：64
'''

'144,140,39,64,387,华南理工大学,杨旭瑜,0'

keyword = ['听力：', '阅读：', '综合：', '写作：', '您的成绩总分：', '学校：', '姓名：', 'End-']

def main():
    file = open('id.txt')
    
    userinfo = []
    
    for line in file:
        id, name = line.split()[0], line.split()[1]
        userinfo.append((id, name))   
        
    for id, name in userinfo:
        i = 0
        for item in GetScore(id, name[0:6]).decode('gbk').split(','):
            print keyword[i],
            print item
            i += 1
            
        
    
        
    
        

if __name__ == '__main__':
    main()


