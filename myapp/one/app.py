from log import *
import logging
from aiohttp import web
import asyncio,json,time,os
from datetime import *
def index(request):
	return web.Response(body=b'<b>2</b>',content_type='text/html')
async def run(loop):
	print(1,len(asyncio.Task.all_tasks()))
	app = web.Application(loop=loop)
	app.router.add_route('get','/',index)
	proctol = app.make_handler()
	print(2,len(asyncio.Task.all_tasks()))
	ser = await loop.create_server(proctol,'127.0.0.1',9000)
	print(3,len(asyncio.Task.all_tasks()))
	logging.info('server start at 127.0.0.1:9000')
	print('start:',ser)
	return ser
loop = asyncio.get_event_loop()

loop.run_until_complete(run(loop))
print(4,len(asyncio.Task.all_tasks()))
loop.run_forever()