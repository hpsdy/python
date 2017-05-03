import functools,inspect
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
					
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
			
