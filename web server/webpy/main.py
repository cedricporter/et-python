#!/usr/bin/env python
# author:  Hua Liang [ Stupid ET ]
# email:   et@everet.org
# website: http://EverET.org
#
import web
import time, traceback, os, hashlib
import charimg

urls = ("/.*", "mainhandler")
app = web.application(urls, globals())

class mainhandler:
    def GET(self):
        return '''<html><body>Please use chrome or firefox...<br/><form method="post" action="" enctype="multipart/form-data">
    Select a picture.<br/><input type="file" name="myfile" value="" />
    <button type="submit">Upload</button>
</form><br/><br/><br/><hr/><a href="https://github.com/cedricporter/et-python/tree/master/web%20server/webpy">Source Code</a> CopyLeft: <a href="http://EverET.org">EverET.org</a></body></html>'''
    def POST(self):
        x = web.input(myfile={})
        if 'myfile' in x: 
            try:
                filepath = x.myfile.filename.replace('\\','/') 
                filename = filepath.split('/')[-1] 
                filename = hashlib.md5(filename).hexdigest() + filename
                fout = open('static/images/'+ filename,'w') 
                fout.write(x.myfile.file.read()) 
                fout.close() 

                pathname = 'static/images/' + filename 
                outfilename = filename + '.html'
                #charimg.make_save_char_img(pathname, 'static/' + outfilename) 
                charimg.save_to_file('static/' + outfilename, charimg.make_char_image('static/images/' + filename).replace('</body>', '<a href="images/' + filename + '">old img</a></body>'))
            except Exception, e:
                print traceback.print_exc() 
                return 'cannot identify image file!' + str(e)
            raise web.seeother('/static/' + outfilename)
        return 'something wrong'

if __name__ == "__main__":
    try: os.mkdir('static')
    except: pass
    try: os.mkdir('static/images')
    except: pass
    app.run()
