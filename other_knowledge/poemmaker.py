import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

import urllib
import json
import datetime
import time

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch("http://www.baidu.com",
                callback=self.on_response)

    def on_response(self, response):
        body=response.body
        self.write(body)
        self.finish()

class GetHandler(tornado.web.RequestHandler):
    def get(self):
        client = tornado.httpclient.HTTPClient()
        res=client.fetch("http://www.baidu.com")
        print(res)
        self.write(res.body)
        self.finish()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler),(r"/g", GetHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()