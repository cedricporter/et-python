# -*-coding:utf-8-*-
# 作者：华亮
#

from Renren import SuperRenren
import time

def main():
    renren = SuperRenren()
    if renren.Create('人人帐号', '密码'):
        #renren.PostMsg(time.asctime())
        #renren.PostGroupMsg('387635422', '%s' % time.asctime())
        #renren.DownloadAlbum('333982368', 'sss')
        renren.DownloadAllFriendsAlbums()
    
if __name__ == '__main__':
    main()
    
