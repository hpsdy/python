import asyncio
from Model import *

class User(Model):
	__table__ = 'user'
	id = intField(pri=True)
	name = strField()
	value = strField()
	
obj = User.findAll()
loop = asyncio.get_event_loop()
db_pool = create_pool(loop,host='10.99.19.39',port='4183',user='root',pwd='123456',db='python')
db = loop.run_until_complete(asyncio.gather(db_pool))
print(db)
loop.run_until_complete(obj)
