#!/usr/bin/env python
#-*- coding:utf-8 -*-
a = {"a":10,"b":20}
if 10 in a.values():
    print('a')

y = None
for x in a.itervalues():
    y = y if y is not None else None
    print(x,":",y)