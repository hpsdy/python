from orm import *
from model import *
import asyncio
async def test(loop):
	db_pool = await create_pool(loop,port=3306,user='root',pwd='',db='python')
	info = await User.findAll()
	print(info)
	await destory_pool()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close() 
