#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# author:  Hua Liang [ Stupid ET ]
# email:   et@everet.org
# website: http://EverET.org
#


from Renren import SuperRenren
import time, os

def main():
    dl, dg = {}, {}
    execfile('user.txt', dg, dl)
    username = dl['username']
    password = dl['password']

    renren = SuperRenren()
    if renren.Create(username, password):
        renren.PostMsg(time.asctime())
        #renren.PostGroupMsg('387635422', '%s' % time.asctime())
        #renren.DownloadAlbum('333982368', 'sss') 
        # renren.DownloadAlbum('285201751', 'cai')
        # renren.DownloadAllFriendsAlbums()
    
if __name__ == '__main__':
    main()
    
