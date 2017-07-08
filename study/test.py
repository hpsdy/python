#-*- coding:utf-8 -*-
import requests
import chardet
import io,sys 
from collections import Iterable,Iterator
from bs4 import BeautifulSoup 
import asyncio
import time
import traceback
print(int(time.time()))
print('test:',__name__)
'''
async def open_f():
	async with open('./mycli.py') as f:
		print(f.read())
loop = asyncio.get_event_loop()
loop.run_until_complete(open_f())
'''
'''
proxy = [
{
'host':'http://123.207.141.60:8080/',
'user':'root',
'pwd':'somepwd',
},
]
def xxx():
	print(len(proxy))
	print(proxy[1])

try:
	xxx()
	raise KeyError('xxx')
except Exception as e:
	print(repr(e))
	print('+++++++++++++++++++')
	print(type(traceback.print_exc()))
	print('+++++++++++++++++++')
	print(type(traceback.format_exc()))
'''
import re
html = '''
<a class='l_post l_post_bright j_l_post clearfix  '>1234</a>
<a class='a'>1</a>
<a class='b'>2</a>
'''
obj = BeautifulSoup(html,'html.parser')
#print(obj.find_all('a',class_=('a','b','c')))
print(obj.find_all('a',class_=re.compile(r'(l_post l_post_bright j_l_post clearfix)[\s]*')))
a = 'aaa'
a+='bbbb'
print(a)