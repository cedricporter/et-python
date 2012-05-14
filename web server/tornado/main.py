#!/usr/bin/env python
import tornado.ioloop, tornado.web
import hashlib, os, time
import charimg

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''<html><body>Please use chrome or firefox...<br/><form method="post" action="" enctype="multipart/form-data">
    Select a picture.<br/><input type="file" name="myfile" value="" />
    <button type="submit">Upload</button>
</form><br/><br/><br/><hr/><a href="https://github.com/cedricporter/et-python/tree/master/web%20server/webpy">Source Code</a> CopyLeft: <a href="http://EverET.org">EverET.org</a></body></html>''')
    def post(self):
        try:
            upload = self.request.files["myfile"][0]
            new_name = hashlib.md5(upload['filename']).hexdigest() + upload['filename']
            pathname = 'static/images/' + new_name

            dst_file = open(pathname, 'wb')
            dst_file.write(upload['body'])
            dst_file.close()

            outfilename = new_name + '.html'
            charimg.make_save_char_img(pathname, 'static/' + outfilename)

            self.redirect('/static/' + outfilename)
        except Exception, e:
            print e
            self.write('cannot identify image file!')

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }
application = tornado.web.Application([
        (r"/", MainHandler),
        ], **settings)

if __name__ == "__main__":
    try: os.mkdir('static')
    except: pass
    try: os.mkdir('static/images')
    except: pass
    application.listen(1758)
    tornado.ioloop.IOLoop.instance().start()
