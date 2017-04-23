from log import *
import logging
from aiohttp import web
import asyncio,json,time,os
from datetime import *
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