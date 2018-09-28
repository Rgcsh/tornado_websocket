import tornado.ioloop
import tornado.web
from tornado import escape
from tornado.httpclient import AsyncHTTPClient
from tornado.routing import HostMatches, Router
from tornado.web import asynchronous
from tornado import locale
from tornado import websocket

class AsydecorHandler(tornado.web.RequestHandler):
	@asynchronous
	def get(self):
		http = AsyncHTTPClient()
		http.fetch("http://dev.zjkgwl.com/", self._on_download)

	def _on_download(self, response):
		x = escape.json_decode(response.body)
		print(x)
		print(response.body)
		self.write("Downloaded!")
		self.finish()


class AbcHandler(tornado.web.RequestHandler):
	def get(self):
		self.write('hello,world!{}'.format(self.xsrf_token))


class MainHandler(tornado.web.RequestHandler):
	def initialize(self, db):
		self.db = db

	def prepare(self):
		print('prepare')

	# return self.finish('EOORE')
	# return self.write_error(404)
	# return self.redirect(r'/one', permanent=False)

	def get(self):
		print(tornado.escape.xhtml_escape('<input />你好！'))
		# print(tornado.escape.xhtml_escape('&lt;input /&gt;你好！'))
		print(tornado.escape.url_escape('http://www.baidu.com'))
		print(tornado.escape.url_unescape('http%3A%2F%2Fwww.baidu.com'))
		print(tornado.escape.json_encode({'name': 2}))
		print(tornado.escape.utf8('today is a good day'))
		print(tornado.escape.to_unicode('你好！'))
		print(tornado.escape.native_str(b'dfdf'))
		print(tornado.escape.squeeze('nihao one two'))

		user_locale = locale.get("es_LA")
		# print(user_locale.translate("Sign out"))

		# people = ['one','two','three']
		people = ['one']
		message = user_locale.translate(
			"%(list)s is online", "%(list)s are online", len(people))
		print(message % {"list": user_locale.list(people)})

		print(self.settings)
		print(self.get_browser_locale(), self.get_status())
		print('_______')
		print(self.get_argument('name'))
		print(self.get_arguments('like'))
		print(self.get_query_argument('name'))
		# print(self.get_body_argument('name'))
		# print(self.get_body_arguments('like'))
		print(self.decode_argument('name'), 'dfdfd')
		print('_______')
		print(self.db)
		print(self.request.headers.get("Content-Type"))
		print(self.request.arguments, self.request.query_arguments, self.request.headers)
		# print(json.loads())

		self.write('hello,world!{}'.format(self.xsrf_token))
		self.set_secure_cookie('_xsrf', self.xsrf_token)
		# self.write_error(404,kwargs={'exc_info':'notfound'})
		self.flush()

	def post(self):
		# print(self.xsrf_form_html())
		print('_______')
		print(self.get_argument('name'))
		print(self.get_arguments('like'))
		print(self.get_body_argument('name'))
		print(self.get_body_arguments('like'))
		print('_______')
		self.write('hello,world')


class AsyHandler(tornado.web.RequestHandler):
	async def get(self):

		if not self.get_secure_cookie('name'):
			self.set_secure_cookie('name', 'rgc')
			self.write('no')
		else:
			self.write('yes')
		import time
		time.sleep(10)

		http = AsyncHTTPClient()
		response = await http.fetch("http://dev.zjkgwl.com")
		print(response)
		json = escape.json_decode(response.body)
		self.write(str(json))


class WebHandler(tornado.websocket.WebSocketHandler):
	# def check_origin(self, origin):
	# 	return True  # 允许WebSocket的跨域请

	def on_message(self, message):
		self.write_message('dfdfdfd')
		# from time import time
		import time
		time.sleep(2)
		self.write_message('two')
		self.close(500,'shutdown')

	def open(self):
		print('open')

	def on_close(self):
		print('on_close')

class HtmlHandler(tornado.web.RequestHandler):
	def get(self):
		print('one')
		self.render("websocket.html")

class Cookie_multi(tornado.web.RequestHandler):
	def get(self):
		if not self.get_secure_cookie('name'):
			self.set_secure_cookie('name', 'rgc')
			self.write('no')
		else:
			print(self.get_secure_cookie('name'))
			self.write('yes')


def make_app():
	settings = {'cookie_secret': 'dfdfdfd',
				'login_url': '/one',
				'xsrf_cookies': True,
				'debug': True}
	database = 'db'
	return tornado.web.Application([
		(r'/', MainHandler, dict(db=database)),
		(r'/one', tornado.web.RedirectHandler,
		 dict(url='http://www.baidu.com', permanent=False)),
		(r'/asy', AsyHandler),
		(r'/web', WebHandler),
		(r'/html', HtmlHandler),
		(r'/asydecor', AsydecorHandler),
		(r'/cookie_multi', Cookie_multi)],
		**settings)


# return tornado.web.Application([
# 	(HostMatches("example.com"), [
# 		(r"/", MainHandler),
# 	]),
# ],**settings)


if __name__ == '__main__':
	app = make_app()
	# app.add_handlers(r'www\.abc\.com',[(r'/abc',AbcHandler)])
	app.listen(8000)
	print(8000)
	tornado.ioloop.IOLoop.current().start()
