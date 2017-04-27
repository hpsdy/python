from log import *
import logging
from aiohttp import web
import asyncio,json,time,os
from datetime import *
import functools
def index(request):
	return web.Response(body=b'<b>2</b>',content_type='text/html')
	
def show_task(n):
	print(n,':',asyncio.Task.all_tasks())
async def run(loop):
	show_task(1)
	app = web.Application(loop=loop)
	app.router.add_route('get','/',index)
	proctol = app.make_handler()
	show_task(2)
	ser = await loop.create_server(proctol,'127.0.0.1',9000)
	show_task(3)
	logging.info('server start at 127.0.0.1:9000')
	print('start:',ser)
	return ser
loop = asyncio.get_event_loop()

#loop.run_until_complete(run(loop))
loop.create_task(run(loop))
show_task(4)
loop.run_forever()


def get(path):
	logging.info('Define decorator @get('/%s')' % path)
	def decorater(func):
	@functools.wraps(func)
		def wrapper(*args,**kw):
			return func(*args,**kw)
		wrapper.__method__ = 'get'
		wrapper.__path__ = path
		return wrapper
	return decorater
def post(path):
	logging.info('Define decorator @post('/%s')' % path)
	def decorater(func):
	@functools.wraps(func)
		def wrapper(*args,**kw):
			return func(*args,**kw)
		wrapper.__method__ = 'post'
		wrapper.__path__ = path
		return wrapper
	return decorater