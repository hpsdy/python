from Model import *
class User(Model):
	__table__ = 'user'
	id = idField(pri=True)
	name = strField()
	
User.findAll()