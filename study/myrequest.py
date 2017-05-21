#-*- coding:utf-8 -*-
import requests
import chardet
import io,sys 
from collections import Iterable,Iterator
from bs4 import BeautifulSoup 
import asyncio
import aiohttp,aiomysql
import random,logging
'''
需要过滤的字符
'''
filter = '[\u0ca5]'
host = 'http://www.qiushibaike.com'
url = host+'/text/page/{0}?s={1}'
'''
代理
'''
proxy = ['http://123.207.141.60:8080/']
async def query(url):
	conn = aiohttp.TCPConnector(limit=50)
	count = len(proxy)
	if count>0:
		random_index = random.randint(0,count-1)
	headers={"Cookie": '''_qqq_uuid_="2|1:0|10:1494948386|10:_qqq_uuid_|56:NDUyY2RjZWRmM2ViZTU1MmRlODZjNDhlN2Q5ZTgyNjk1ODZjNDYxMQ==|8f70e6e7ecaa91941eb1acb75783419282af1715d4ef390c0554a9c65afea52e"; __cur_art_index=6400; _xsrf=2|bdadfff7|a64a26176df54659196af500457394c0|1495344490; Hm_lvt_2670efbdd59c7e3ed3749b458cafaa37=1494948394,1494949487,1495115207,1495344493; Hm_lpvt_2670efbdd59c7e3ed3749b458cafaa37=1495348175; _ga=GA1.2.875152845.1494948395; _gid=GA1.2.1955986889.1495348176; _gat=1''',"User-Agent":'''Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'''}
	async with aiohttp.ClientSession(headers=headers,connector=conn) as session:
		if not count:
			async with session.get(url) as resp:
				cur_url = resp.url
				pre_url = None			
				if resp.history:
					pre_url = resp.history[0].url
				if pre_url and cur_url!=pre_url:
					return None
				html = await resp.text()		
		else:
			async with session.get(url,proxy=proxy[random_index]) as resp:
				cur_url = resp.url
				pre_url = None
				if resp.history:
					pre_url = resp.history[0].url
				cur_url = str(cur_url)[:-10]
				cur_url = cur_url.strip('''/''')
				pre_url = str(pre_url)[:-10]
				pre_url = pre_url.strip(''''/''')
				logging.warning('%s:%s' %(cur_url,pre_url))
				if pre_url and cur_url!=pre_url:					
					return None				
				html = await resp.text()		
		
	return html

data = {}
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
	#global data
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
				gender = '男' if gender=='manIcon' else '女'
			else:
				gender = '未知'
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
	pool = await aiomysql.create_pool(host='localhost',port=3306,user='root',password='',maxsize=10,minsize=1,db='python',loop=loop)
	return pool
async def main(loop):
	pool = await mysql_epool(loop)
	html = await query(url.format(10,random_a(7)))
	html = html.replace(filter,'')
	if not html:
		return None
	ret = BeautifulSoup(html,'html.parser')
	
	list  = ret.find_all('div',class_='article block untagged mb15')
	get_list(list)
if __name__ == '__main__':
	run_loop = (x for x in range(1,100000))
	for i in run_loop:
		pass
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main(loop))
	print(data)