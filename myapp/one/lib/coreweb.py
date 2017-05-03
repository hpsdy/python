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
	��ȡû��Ĭ��ֵ�������ؼ��ֲ���
	'''
	args = []
	params = inspect.signature(fn).parameters
	for name,param in params.items():
		if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
			args.append(name)
	return tuple(args)
def get_named_kw_args(fn):
	'''
	��ȡ���е������ؼ��ֲ���
	'''
	args = []
	params = inspect.signature(fn).parameters
	for name,param in params.items():
		if param.kind == inspect.Parameter.KEYWORD_ONLY:
			args.append(name)
	return tuple(args)
def has_named_kw_args(fn):
	'''
	�ж��Ƿ��������ؼ��ֲ���
	'''
	args = []
	params = inspect.signature(fn).parameters
	for name,param in params.items():
		if param.kind == inspect.Parameter.KEYWORD_ONLY:
			return True
			
def has_var_kw_args(fn):
	'''
	�ж��Ƿ��ǹؼ��ֲ���
	'''
	args = []
	params = inspect.signature(fn).parameters
	for name,param in params.items():
		if param.kind == inspect.Parameter.VAR_KEYWORD:
			return True
	
def has_request_args(fn):
	'''
	�Ƿ�������������������Ϊ���һ����������
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
			
