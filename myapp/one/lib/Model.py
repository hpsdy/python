import asyncio
from orm import *

class User(Model):
	__table__ = 'user'
	id = intField(pri=True)
	name = strField()
	values = strField()
	


