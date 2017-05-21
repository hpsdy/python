#-*- coding:utf-8 -*-
import requests
import chardet
import io,sys 
from collections import Iterable,Iterator
from bs4 import BeautifulSoup 
import asyncio
async def open_f():
	async with open('./mycli.py') as f:
		print(f.read())
loop = asyncio.get_event_loop()
loop.run_until_complete(open_f())