#!/usr/bin/env python
#-*- coding:utf-8 -*-
import unittest,time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
url = 'https://www.baidu.com/'

class xpage(unittest.TestCase):
    base_dir = './html'
    def setUp(self):
        self.driver = webdriver.PhantomJS()
    def test_query(self):
        try:
            driver = self.driver
            driver.get(url)
            elem = driver.find_element(By.NAME,'wd')
            elem.send_keys('中国',Keys.RETURN)
            locator = (By.XPATH,"//div[contains(@class,'result c-container')]")
            wait = EC.presence_of_element_located(locator)
            WebDriverWait(driver,10).until(wait)
            html = driver.page_source
            ctime = time.time()
            ctime = str(int(int(ctime)*1000))
            file = "%s/%s.html" % (self.base_dir,ctime)
            with open(file,'ba') as fn:
                fn.write(html.encode('utf-8'))
        except Exception as e:
            print("Exception:%s" % repr(e))
    def tearDown(self):
        self.driver.close()
        print('end')
if __name__=='__main__':
    unittest.main()