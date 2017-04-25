from orm import *
from model import *
import asyncio
async def test(loop):
	global _pool
	db_pool = await create_pool(loop,host='10.99.19.39',port=8686,user='root',pwd='123456',db='python')
	print(db_pool)
	info = await User.findAll()
	print(info)
	print(_pool)
	await destory_pool()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close() 
