#-*- coding:utf-8 -*-
import logging
import log,sys,os
logger = logging.getLogger('mylog')
logger.warning('yyy')

print(os.path.abspath(os.path.dirname(__file__)))