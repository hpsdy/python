#!/usr/bin/env python
#-*- coding:utf-8 -*-
from pyquery import PyQuery as pq
import os,sys,locale


def scan_dir(dir):
    files = []
    if os.path.isdir(dir):
        list = os.listdir(dir)
        if list:
            for _file in list:
                tmp = "%s/%s" %(dir,_file)
                if os.path.isfile(tmp):
                    files.append(tmp)
    return files
dir = './html'
files = scan_dir(dir)
print(files)
for file in files:
    with open(file,'br') as fn:
        bstr = fn.read()
        str = bstr.decode()
        html = pq(str)
        div = html("div[class!='result c-container' ]")
        for line in div.items():
            h = line("h3[class='t']")
            if not h :
                continue
            a = h('a')
            title = a.text()
            href = a.attr('href')
            print(title,href)
            break