#-*- coding:utf-8 -*-
import requests
import chardet
import io,sys 
from collections import Iterable,Iterator
from bs4 import BeautifulSoup 
host = 'http://www.qiushibaike.com'
url = host+'/text/page/{0}'
def query(url):
	ret = requests.get(url)
	html = ret.text
	return html

html = query(url.format(1))
ret = BeautifulSoup(html,'html.parser')
list  = ret.find_all('div',class_='article block untagged mb15')
data = []
def all_content(content):
	tmpContent = []
	for line in content:
		tmpContent.append(line)
	content = "\n".join(tmpContent)
	return content
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
		data.append(tmp)
	except Exception:
		continue
print(data)