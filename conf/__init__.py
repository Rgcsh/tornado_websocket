import os

from conf.local import *


class Config(object):
	_keys = list(filter(lambda x: x.isupper(), globals().keys()))

	____ = dict(
		zip(
			_keys,
			map(lambda x: globals()[x], _keys)
		)
	)

	@classmethod
	def get(cls, item):
		return cls.____.get(item) or cls.____.get(item.upper())

	@classmethod
	def set(cls, name, val):
		cls.____[name.upper()] = val

	@classmethod
	def to_dict(cls):
		return cls.____
