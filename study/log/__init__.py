#-*- coding:utf-8 -*-
import logging
import logging.config
logging.captureWarnings(True)
logging.config.fileConfig('./log/logging.conf')
logger = logging.getLogger('root.mylog')
