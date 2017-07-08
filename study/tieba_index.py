#-*- coding:utf-8 -*-
import requests
import asyncio
import aiohttp
import os,re,traceback
from bs4 import BeautifulSoup
url='https://tieba.baidu.com/p/{0}?see_lz={1}&pn={2}'
from log import logger
class TIEBA(object):
	file_dir = './file'
	def __init__(self,size=0,only_lz=True,all=False):
		self.url = url
		self.size = size
		self.see_lz = only_lz
		self.all = all
	def quert_by_url(self,url):
		try:
			logger.warning('url:%s' % url)
			html = requests.get(url,verify=False)
			return html.text
		except Exception as e:
			logger.warning(repr(e))
			return None
	def data(self,page = 1):
		see_lz = 1 if self.see_lz else 0
		page = page if str(page).isdigit() else 1
		url = self.url.format(self.size,see_lz,page)
		html = self.quert_by_url(url)
		if not html:
			logger.warning('url:%s,ret is None' % url)
			return None
		try:		
			ret = BeautifulSoup(html,'html.parser')		
			page_num = ret.find('li',class_='l_reply_num').find_all('span',class_='red')[1].string
			data_str = self.page_data(ret,page)
			self.write(data_str,self.size,page)
			if self.all and int(page)<int(page_num):
				for i in range(int(page)+1,int(page_num)+1):
					url = self.url.format(self.size,see_lz,i)
					html = self.quert_by_url(url)
					if not html:
						logger.warning('url:%s,ret is None' % url)
						continue
					ret = BeautifulSoup(html,'html.parser')					
					data_str = self.page_data(ret,i)
					self.write(data_str,self.size,i)
		except Exception as e:
			logger.warning(traceback.format_exc())
	def page_data(self,data,page):
		tmp_data = ''
		lou_info = data.find_all('div',class_=re.compile(r'(l_post l_post_bright j_l_post clearfix)[\s]*'))
		if not lou_info:
			return tmp_data
		else:
			for div in lou_info:
				
				lou_nums = div.find_all('span',class_='tail-info')
				for lou_num in lou_nums:
					lou_num = lou_num.string
					if lou_num and lou_num.endswith('楼'):
						break;
				auth = div.find('li',class_='d_name').find('a').string
				content = div.find('div',class_=re.compile(r'(d_post_content j_d_post_content)[\s]+')).strings
				content = self.all_content(content)		
				if not lou_num or not auth or not content:
					continue
				tmp_data += '-----'+str(lou_num)+'-----'
				tmp_data += "\n"
				tmp_data += "楼层："+lou_num+"\n"
				tmp_data += "auth："+auth+"\n"
				tmp_data += "content："+content+"\n"
			return tmp_data
				
	def all_content(self,content):
		tmpContent = []
		for line in content:
			tmpContent.append(line)
		content = "\n".join(tmpContent)
		return content
	def write(self,data,size,page):
		if not os.path.exists(self.file_dir):
			os.mkdir(self.file_dir)
		sizedir = os.path.join(self.file_dir,str(size))
		if not os.path.exists(sizedir):
			os.mkdir(sizedir)
		filename = os.path.join(sizedir,str(page))
		with open(filename,'wb') as fn:
			fn.write(data.encode())
size = input('please input url size:')
size = int(size)
only_lz = input('only_lz?')
only_lz = bool(only_lz)
all = input('is_all?')
all = bool(all)	
page = input('page:')
page = int(page)
#tieba = TIEBA(3138733512,True,all=True)
#tieba.data(1)
tieba = TIEBA(size,only_lz,all=all)
tieba.data(page)

