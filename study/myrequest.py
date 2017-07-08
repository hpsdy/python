#-*- coding:utf-8 -*-
import requests
import chardet
import io,sys 
from collections import Iterable,Iterator
from bs4 import BeautifulSoup 
import asyncio
import aiohttp,aiomysql
import random,logging
import time,copy
logging.basicConfig(level=logging.DEBUG)
DIVISION = ','
is_end = False
#数据库连接池
_pool = None
'''
需要过滤的字符
'''
filter = '[\u0ca5|\u03be]'
host = 'http://www.qiushibaike.com'
url = host+'/text/page/{0}?s={1}'
data = {}
'''
代理
'''
proxy = [
{
'host':'http://123.207.141.60:8080/',
'user':'root',
'pwd':'somepwd',
},
]
async def query(qurl,loop,page=1):
	global proxy
	conn = aiohttp.TCPConnector(limit=50)
	count = len(proxy)
	proxy_auth = None
	proxy_host = None
	if count>0:
		random_index = random.randint(0,count-1)
		proxy_info = proxy[random_index]
		proxy_auth = aiohttp.BasicAuth(proxy_info['user'],proxy_info['pwd'])
		proxy_host = proxy_info['host']
	headers={"Cookie": '''_qqq_uuid_="2|1:0|10:1494948386|10:_qqq_uuid_|56:NDUyY2RjZWRmM2ViZTU1MmRlODZjNDhlN2Q5ZTgyNjk1ODZjNDYxMQ==|8f70e6e7ecaa91941eb1acb75783419282af1715d4ef390c0554a9c65afea52e"; __cur_art_index=6400; _xsrf=2|bdadfff7|a64a26176df54659196af500457394c0|1495344490; Hm_lvt_2670efbdd59c7e3ed3749b458cafaa37=1494948394,1494949487,1495115207,1495344493; Hm_lpvt_2670efbdd59c7e3ed3749b458cafaa37=1495348175; _ga=GA1.2.875152845.1494948395; _gid=GA1.2.1955986889.1495348176; _gat=1''',"User-Agent":'''Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'''}
	async with aiohttp.ClientSession(headers=headers,connector=conn,loop=loop) as session:
		
		async with session.get(qurl,proxy=proxy_host,auth=proxy_auth) as resp:
			cur_url = resp.url
			pre_url = None
			if resp.history:
				pre_url = resp.history[0].url
			cur_url = str(cur_url)[:-10]
			cur_url = cur_url.strip('''/''')
			pre_url = str(pre_url)[:-10]
			pre_url = pre_url.strip(''''/''')	
			if pre_url and cur_url!=pre_url and page!=1:			
				logging.warning('cur:%s||pre:%s' %(cur_url,pre_url))		
				return None					
			html = await resp.text()
	return html


def all_content(content):
	tmpContent = []
	for line in content:
		tmpContent.append(line)
	content = "\n".join(tmpContent)
	return content
def random_a(len):
	num = random.random()
	num *= 10**10
	num = str(num)
	return num[:7]
def get_list(list):
	global data
	for x in list:
		try:
			tmp = {}
			head = x.find('div',class_='author clearfix',recursive=False)
			title = head.h2.string
			gender = head.find('div',class_='articleGender',recursive=False)
			if gender:
				age = gender.string
				gender = gender['class'].pop(1)
				gender = gender.strip()
				gender = '1' if gender=='manIcon' else '2'
			else:
				gender = '0'
			detail = x.find('a',class_='contentHerf')
			href = detail['href']
			id = href.split('/').pop() if href else 0
			if id == 0:
				continue
			hadMore = x.find('div',class_='content').find('span',class_='contentForAll')
			if hadMore:
				href = '/'.join(href.split('/'))
				detailUrl = host+'/'+href
				detail = query(detailUrl)
				detail = BeautifulSoup(detail,'html.parser')
				content = detail.find('div',class_='article block untagged noline mb15').find('div',class_='content').strings
			else:
				content = x.find('div',class_='content').span.strings
			content = all_content(content) if content else ''
			num = x.find('span',class_='stats-vote').i.string
			tmp['id'] = id
			tmp['title'] = title
			tmp['gender'] = gender
			tmp['age'] = age
			tmp['content'] = content
			tmp['likeNum'] = num
			if id not in data:
				data[id] = tmp
		except Exception:
			continue
	return data
async def mysql_epool(loop):
	global _pool
	_pool = await aiomysql.create_pool(host='localhost',port=3306,user='root',password='',maxsize=10,minsize=1,db='qiushi',loop=loop,charset='utf8',autocommit=True)
	return _pool
async def insert_joke(arr):
	global data
	global _pool
	_table = 'qiu_joke'
	ntime = int(time.time())
	arr['time'] = ntime
	map = {
	'id':'id',
	'title':'name',
	'gender':'gender',
	'age':'age',
	'likeNum':'like_num',
	'content':'content',
	'time':'time',
	}
	
	sql = 'insert %s (%s) values(%s) on duplicate key update %s'
	field = []
	values = []
	setStr = []
	for x,val in arr.items():
		key = map[x]
		key = '`%s`' % key
		val = "'%s'" % val
		field.append(key)
		values.append(val)
		str = '%s = %s' % (key,val)
		setStr.append(str)
	field = DIVISION.join(field)
	values = DIVISION.join(values)
	setStr = DIVISION.join(setStr)
	sql = sql % (_table,field,values,setStr)
	logging.info('sql:%s' % sql)
	try:
		async with _pool.get() as conn:
			async with conn.cursor() as cur:
				await cur.execute(sql)
				affected = cur.rowcount
				if affected:
					data.pop(arr['id'])
				print('sql ret:',affected)						
	except Exception as e:
		logging.info('except:%s' % repr(e))	
		return ''
async def main(loop):
	global is_end
	run_loop = (x for x in range(1,100))
	for i in run_loop:
		rurl = url.format(i,random_a(7))
		logging.info('url:%s' % rurl)
		html = await query(rurl,loop,i)
		if not html:			
			break
		html = html.replace(filter,'')
		ret = BeautifulSoup(html,'html.parser')
		list  = ret.find_all('div',class_='article block untagged mb15')
		get_list(list)
	is_end = True	
async def close_pool():
	global _pool
	_pool.close()
	await _pool.wait_closed()
async def sync_data(loop):
	global data
	global is_end
	global _pool
	if not _pool:
		_pool = await mysql_epool(loop)
	while(True):
		if data:
			logging.info('data is not null')
			datax = copy.copy(data)
			for x,y in datax.items():
				await insert_joke(y)
		elif is_end:
			logging.info('loop is end')
			await close_pool()
			break
		else:
			logging.info('waiting for data')
			await asyncio.sleep(2)
			
if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	task = []
	task.append(main(loop))
	task.append(sync_data(loop))
	loop.run_until_complete(asyncio.gather(*task))
	#print(data)
	