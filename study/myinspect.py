import inspect
import os
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

print(__file__,os.path.abspath(__file__),os.path.dirname(os.path.abspath(__file__)),path)

'''
def add_routes(module_name):
	n = module_name.rfind('.')
	print(n)
	if n == (-1):
		mod = __import__(module_name, globals(), locals())
	else:
		name = module_name[n+1:]
		mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
	print(mod)
	for attr in dir(mod):
		fn = getattr(mod, attr)
		print(attr,':',fn)
		if attr.startswith('_'):
			continue
		fn = getattr(mod, attr)
		#print('fn:',fn)
		if callable(fn):
			method = getattr(fn, '__method__', None)
			path = getattr(fn, '__route__', None)
add_routes('handlers')











def a(a, b=0, *c, d, e=1, **f):
	pass

aa = inspect.signature(a)
print("inspect.signature（fn)是:%s" % aa)
print("inspect.signature（fn)的类型：%s" % (type(aa)))
print("\n")
bb = aa.parameters
print("signature.paramerters属性是:%s" % bb)
print("ignature.paramerters属性的类型是%s" % type(bb))
print("\n")
print("inspect.Parameter.KEYWORD_ONLY属性是:%s" % inspect.Parameter.KEYWORD_ONLY)
print("inspect.Parameter.empty属性是%s" % inspect.Parameter.empty)
print("\n")
for cc, dd in bb.items():
	print("mappingproxy.items()返回的两个值分别是：%s和%s" % (cc, dd))
	print("mappingproxy.items()返回的两个值的类型分别是：%s和%s" % (type(cc), type(dd)))
	print("\n")
	ee = dd.kind
	print("Parameter.kind属性是:%s" % ee)
	print("Parameter.kind属性的类型是:%s" % type(ee))
	print("\n")
	gg = dd.default
	print("Parameter.default的值是: %s" % gg)
	print("Parameter.default的属性是: %s" % type(gg))
	print("\n")


ff = inspect.Parameter.KEYWORD_ONLY
print("inspect.Parameter.KEYWORD_ONLY的值是:%s" % ff)
print("inspect.Parameter.KEYWORD_ONLY的类型是:%s" % type(ff))
'''