from common import *
import aiomysql
import asyncio
from orm import *

async def create_pool(loop,**kw):
	global _pool
	_pool = await aiomysql.create_pool(
		host = kw.get('host','localhost'),
		port = kw.get('port',3306),
		user = kw['user'],
		password = kw['pwd'],
		db = kw['db'],
		charset = kw.get('charset','utf8'),
		autocommit = kw.get('autocommit',True),
		maxsize = kw.get('max',10),
		minsize = kw.get('min',2),
		loop=loop,
	)
	return _pool
async def destory_pool():
	global _pool
	if _pool is not None:
		_pool.close()
		await _pool.wait_closed()
async def select(sql,argv,size=None):
	global _pool
	with await _pool as conn:
		cur = await conn.cursor()
		await cur.execute(sql.replace('?','%s'),argv)
		if size:
			ret = await cur.fetchmany(size)
		else:
			ret = await cur.fetchall()
		await cur.close()
	return ret
		
async def execute(sql,argv):
	global _pool
	with await _pool as conn:
		cur = await conn.cursor()
		await cur.execute(sql.replace('?','%s'),argv)
		effected = cur.rowcount
		await cur.close()
	return effected


class ModelMetaClass(type):
	def __new__(obj,classname,bases,attrs):
		print('xxx:',obj,'xxx',type(obj),'xxx',classname,'xxx',bases,'xxx',attrs)
		if classname == 'Model':
			return type.__new__(obj,classname,bases,attrs)
		tableName = attrs.get('__table__',None) or name
		mapping = dict()
		fields = []
		priKey = None
		for x,y in attrs.items():
			if isinstance(y,field):
				mapping[x] = y
				if y.pri:
					if priKey:
						raise RuntimeError('duplicate pri key:%s' % priKey)
					else:
						priKey = x
				else:
					fields.append(x)
		if not priKey:
			raise RuntimeError('pri key not exist')
		for n in mapping.keys():
			attrs.pop(n)
		escepted_fields = list(map(lambda f:'`%s`' % f,fields))
		attrs['__mapping__'] = mapping
		attrs['__table__'] = tableName
		attrs['__primary_key__'] = priKey
		attrs['__fields__'] = fields
		attrs['__select__'] = 'select `%s`,%s from `%s`' % (priKey,','.join(escepted_fields),tableName)
		attrs['__insert__'] = 'insert `%s` (`%s`,%s) values(%s)' %(tableName,priKey,','.join(fields),create_args_string(len(escepted_fields)+1))
		attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName,','.join(map(lambda f:'`%s`=?' % f,fields)),priKey)
		attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName,priKey)
		return type.__new__(obj,classname,bases,attrs)

class Model(dict,metaclass=ModelMetaClass):
	a = 10
	def __init__(self,**kw):
		super(Model,self).__init__(**kw)
	def __getattr__(self,name):
		try:
			return self[name]
		except KeyError:
			raise AttributeError('%s key is not exist' % name)
	def __setattr__(self,name,val):
		self[name] = val
	def getValue(self,name):
		return getattr(self,name,None)
	def getValueOrDefault(self,name):
		value = getattr(self,name,None)
		if value is None:
			field = self.__mapping__[name]
			if field.default is not None:
				value = field.default() if callable(field.default) else field.default
				setattr(self,name,value)
		return values
	@classmethod
	async def findAll(cls,where=None,args = None,**kw):
		sql = cls.__select__
		return await select(sql,[])
class field(object):
	def __init__(self,name,type,pri,default):
		self.name = name
		self.type = type
		self.pri = pri
		self.default = default
	def __str__(self):
		return '<%s,%s:%s>' % (self.__class__.__name__,self.name,self.type)

class strField(field):
	def __init__(self,name=None,type='varchar(100)',pri=False,default=None):
		super(strField,self).__init__(name,type,pri,default)
class intField(field):
	def __init__(self,name=None,type='int(11)',pri=False,default=None):
		super(intField,self).__init__(name,type,pri,default)
		
		

