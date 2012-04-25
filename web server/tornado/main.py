#!/usr/bin/env python
import tornado.ioloop, tornado.web
import hashlib, os, time
import charimg

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''<html><body>Please use chrome or firefox...<br/><form method="post" action="" enctype="multipart/form-data">
    <input type="file" name="upload" value="" />
    <button type="submit">Upload</button>
</form></body></html''')
    def post(self):
        try:
            upload = self.request.files["upload"][0]
            new_name = hashlib.md5(upload['filename']).hexdigest() + upload['filename']
            pathname = 'static/images/' + new_name

            dst_file = open(pathname, 'wb')
            dst_file.write(upload['body'])
            dst_file.close()

            outfilename = new_name + '.html'
            charimg.make_save_char_img(pathname, 'static/' + outfilename)

            self.redirect('/static/' + outfilename)
        except:
            self.write('cannot identify image file!')

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }
application = tornado.web.Application([
        (r"/", MainHandler),
        ], **settings)

if __name__ == "__main__":
    application.listen(1758)
    tornado.ioloop.IOLoop.instance().start()
