import web

class index():
    def GET(self):
        return '1' * 100

urls = ('/', 'index')

print 'a' * 1000
if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
