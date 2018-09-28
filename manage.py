import redis
import tornado.httpserver
import tornado.ioloop
import tornado.web
from motor import motor_tornado
from tornado import websocket
from tornado.gen import coroutine

from conf import Config


class WebHandler(websocket.WebSocketHandler):
	# 在线用户dict
	all_user = {}

	def initialize(self, mongo, redis):
		self.mongo = mongo
		self.redis = redis

	@property
	def db(self):
		return self.mongo.get_database('rgc')

	@property
	def col(self):
		return self.db.get_collection('web')

	def check_origin(self, origin):
		return True  # 允许WebSocket的跨域请求

	@coroutine
	def on_message(self, message):
		#因为没有登录相关功能，每次传输都 用 # 拼接 发送者，消息，接受者
		resu = str.split(message, '#')

		name = resu[0]
		val = resu[1]
		to = resu[2]
		# 判断对方是否在线
		if 'name:{}'.format(to) not in list(self.all_user.keys()):
			self.write_message('Out Line')
			# 存储消息到db
			# if not self.redis.hget('name_list', '{}:{}'.format(name, to)):
			# 	self.redis.hset('name_list', '{}:{}'.format(name, to), 1)
			self.col.insert({'name': '{}:{}'.format(name, to), 'msg': val})
		else:
			# 发送最新消息
			self.all_user['name:{}'.format(to)].write_message(val)

		# 检查是不是第一次上线
		if 'name:{}'.format(name) not in list(self.all_user.keys()):
			# 给自己发送历史消息
			his_one = self.col.find({'name': '{}:{}'.format(to, name)}, {'msg': 1, '_id': 0})
			for it in (yield his_one.to_list(100)):
				self.write_message(it['msg'])
		# 删除历史消息
		self.col.delete_many({'name': '{}:{}'.format(to, name)})
		# 单点登录聊天
		self.all_user.update({'name:{}'.format(name): self})
		# 发给自己
		self.write_message('send success')

	def open(self):
		pass

	def on_close(self):
		# 当客户端关闭连接时，去除内存中保存的用户，让其离线
		key = None
		for k, v in self.all_user.items():
			if v == self:
				key = k
				break
		if key:
			self.all_user.pop(key)
		print('{} out line'.format(key))


class HtmlHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("static/index.html")


class StaticHandler(tornado.web.RequestHandler):
	def get(self, file_url):
		self.render("static/{}".format(file_url))


def make_app():
	settings = {'cookie_secret': 'dfdfdfd',
				'xsrf_cookies': True,
				'debug': True}
	other_db = {'mongo': motor_tornado.MotorClient(**Config.get('MONGO_CONF')),
				'redis': redis.StrictRedis()}
	return tornado.web.Application([
		(r'/web', WebHandler, other_db),
		(r'/', HtmlHandler),
		(r'/static/(.*)', StaticHandler)
	], **settings)


if __name__ == '__main__':
	app = make_app()
	http_server = tornado.httpserver.HTTPServer(app)
	ip='127.0.0.1'
	port = 8000
	http_server.bind(8000, ip)
	http_server.start(1)
	print('server start! http://{}:{}'.format(ip, port))
	tornado.ioloop.IOLoop.current().start()
