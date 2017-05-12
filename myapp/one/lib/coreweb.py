from log import *
import logging
import asyncio, os, inspect,functools
from urllib import parse
from aiohttp import web
from apis import APIError

def get(path):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args,**kw):
			return func(*args,**kw)
		wrapper.__method__ = 'GET'
		wrapper.__route__ = path
		return wrapper
	return decorator
def post(path):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args,**kw):
			return func(*args,**kw)
		wrapper.__method__ = 'POST'
		wrapper.__route__ = path
		return wrapper
	return decorator
def get_required_kw_args(fn):
	'''
	获取没有默认值的命名关键字参数
	'''
	args = []
	params = inspect.signature(fn).parameters
	for name,param in params.items():
		if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
			args.append(name)
	return tuple(args)
def get_named_kw_args(fn):
	'''
	获取所有的命名关键字参数
	'''
	args = []
	params = inspect.signature(fn).parameters
	for name,param in params.items():
		if param.kind == inspect.Parameter.KEYWORD_ONLY:
			args.append(name)
	return tuple(args)
def has_named_kw_args(fn):
	'''
	判断是否是命名关键字参数
	'''
	args = []
	params = inspect.signature(fn).parameters
	for name,param in params.items():
		if param.kind == inspect.Parameter.KEYWORD_ONLY:
			return True
			
def has_var_kw_args(fn):
	'''
	判断是否是关键字参数
	'''
	args = []
	params = inspect.signature(fn).parameters
	for name,param in params.items():
		if param.kind == inspect.Parameter.VAR_KEYWORD:
			return True
	
def has_request_args(fn):
	'''
	是否有请求参数且请求参数为最后一个命名参数
	'''
	sig = inspect.signature(fn)
	params = sig.parameters
	found = False
	for name,param in params.items():
		if name == 'request':
			found = True
			continue
		if found and (param.kind!=inspect.Parameter.VAR_KEYWORD and param.kind!=inspect.Parameter.KEYWORD_ONLY and param.kind!=inspect.Parameter.VAR_KEYWORD):
			raise KeyError('request is error')
	return found
	
	
	
	
	
	
	
class RequestHandler(object):
	def __init__(self,app,fn):
		self._app = app
		self._func = fn
		self._has_request_args = has_request_args(fn)
        self._has_var_kw_args = has_var_kw_args(fn)
        self._has_named_kw_args = has_named_kw_args(fn)
        self._named_kw_args = get_named_kw_args(fn)
        self._required_kw_args = get_required_kw_args(fn)
	def __call__(self,request):
		kw = None
		if self._has_var_kw_args or self._has_named_kw_args or self._has_request_args:
			if request.method == 'POST':
				if not request.content_type:
					return web.HTTPBadRequest('miss http content_type')
				ct = request.content_type.lower()
				if ct.startswith('application/json'):
					params = await request.json()
					if not isinstance(params,dict):
						return web.HTTPBadRequest('bad json object')
					kw = params
				elif ct.startswith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
					params = await request.post()
					kw = dict(**params)
				else:
					return web.HTTPBadRequest('Unsupported content_type:%s' % request.content_type)
			if request.method == 'GET':
				qs = request.query_string
				if qs:
					kw = dict()
					for x,y in parse.parse_qs(qs,True).items():
						kw[x] = y[0]
		if not kw:
			kw = dict(**request.match_info)
		else:
			if not self._has_var_kw_args and self._named_kw_args:
				copy = dict()
				for name in self._named_kw_args:
					if name in kw:
						copy[name] = kw[name]
				kw = copy
			for name,val in request.match_info.items():
				if name in kw:
					logging.warning('duplicate key:%s' % name)
				kw[name] = val
		if self._has_request_args:
			kw['request'] = request
		if self._required_kw_args:
			for name in self._required_kw_args:
				if not  name in kw:
					return web.HTTPBadRequest('miss must param:%s' % name)
		try:
			ret = self._func(**kw)
			return ret
		except APIError as e:
			return dict(error=e.error, data=e.data, message=e.message)
			
def add_static(app):
	path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'static')
	app.router.add_static('/static/',path)

def add_route(app):
	
	
	
	
	
	
	
	
	
	
			
