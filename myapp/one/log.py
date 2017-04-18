import logging
import time
from datetime import *
now = datetime.now().strftime('%Y%m%d%H')
filename = './log/log.'+now
logging.basicConfig(level=logging.INFO ,filename=filename)