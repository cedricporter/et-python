# -*-coding:utf-8-*-
# 作者：华亮
#

import urllib
import urllib2
import re
from HTMLParser import HTMLParser


# 获取QQ空间博客列表
class QQBlogList(HTMLParser):
    in_key_div = False
    in_ul = False
    in_li = False
    in_a = False
    blogList = []
    lasturl = ''
    
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'div' and 'class' in attrs and attrs['class'] == 'bloglist':
            self.in_key_div = True
        elif self.in_key_div:
            if tag == 'ul':
                self.in_ul = True
            elif self.in_ul and tag == 'li':
                self.in_li = True
            elif self.in_li and tag == 'a' and 'href' in attrs:
                self.in_a = True
                self.lasturl = attrs['href']
    
    def handle_data(self, data):
        if self.in_a:
            self.blogList.append((data, self.lasturl))
    
    def handle_endtag(self, tag):
        if self.in_key_div and tag == 'div':
            self.in_key_div = False
        elif self.in_ul and tag == 'ul':
            self.in_ul = False
        elif self.in_li and tag == 'li':
            self.in_li = False
        elif self.in_a and tag == 'a':
            self.in_a = False
            
         
            
class QQ:  
    '''
    QQ
        作者：华亮
        说明：自动下载QQ空间博客文章
    '''
        
    @staticmethod      
    def DownloadBlog(qq, filename = None):
        print 'Start'
        blogurl = 'http://qz.qq.com/%s/bloglist?page=0' % qq
        QQ.__Download(blogurl, filename)           
        print 'End'
    
    @staticmethod
    def __Download(starturl, filename):
        url = starturl
        
        cookieFile = urllib2.HTTPCookieProcessor()
        opener = urllib2.build_opener(cookieFile)    
        
        # 获取所有页的文章路径
        while True:
            req = urllib2.Request(url)
            result = opener.open(req)        
            text = result.read()     
            
            qq = QQBlogList()        
            qq.feed(text)
            qq.close()          
                   
            nextpagePattern = re.compile(r'<a href="(.*?)" title="下一页" class="bt_next"><span>下一页</span></a>')              
            nextpage = nextpagePattern.search(text)
            if nextpage:
                url = nextpage.group(1)            
            else:
                break  
          
        if not filename:
            filename = "blog.txt"
        file = open(filename, 'w')    
        
        # 下载文章
        blogContentPattern = re.compile(r'<div class="entry_content">(.*?)</div>', re.S) 
        for title, url in qq.blogList:
            print 'Downloading', title
            req = urllib2.Request(url)
            result = opener.open(req)
            file.write('\n' + title + '\n')
            ret = blogContentPattern.search( result.read() )
            if ret:
                file.write(ret.group(1).replace('<p>', '\n'))
        file.close()
            
