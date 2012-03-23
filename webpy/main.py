import web

urls = ("/.*", "hello")
app = web.application(urls, globals())

class hello:
    def GET(self):
        return '<html><body><h1>Hello, EverET.org.</h1></body></html>'

if __name__ == "__main__":
    app.run()
