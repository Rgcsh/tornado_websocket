import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from pymongo import MongoClient

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
	def __init__(self):
		handlers = [(r"/(\w+)", WordHandler)]
		conn = MongoClient(host='47.96.1.64', port=27017, username='simple', password='simple.mongo.dev'
						   , authSource='UserExt'
						   )

		self.db = conn["UserExt"]
		tornado.web.Application.__init__(self, handlers)


from tornado.httpclient import AsyncHTTPClient


async def asywordhandler(url):
	print('34')
	http_client = AsyncHTTPClient()
	response = await http_client.fetch(request=url)
	print('ddfdfdf', response.body)
	return response


def call(result):
	print('dfdfdf', result)


class WordHandler(tornado.web.RequestHandler):
	def get(self, word):
		coll = self.application.db.words
		word_doc = coll.find_one({"uid": 111})
		x = asywordhandler(url='http://dev.zjkgwl.com')
		print(x, 'dfdf')
		if word_doc:
			del word_doc["_id"]
			self.write(word_doc)
		else:
			self.set_status(404)
			self.write({"error": "word not found"})


if __name__ == "__main__":
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	print(options.port)
	tornado.ioloop.IOLoop.instance().start()
