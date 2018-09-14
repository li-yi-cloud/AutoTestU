'''
Created on 2018年7月16日

@author: cloud
'''
from appium import webdriver
import time
import logging

logger = logging.getLogger()

class IDriver():
    '''custom remote appium driver object.'''
    def __init__(self,command_executor='http://127.0.0.1:4723/wd/hub',desired_capabilities=None, browser_profile=None, proxy=None, keep_alive=False):
        self.__driver=webdriver.Remote(command_executor,desired_capabilities, browser_profile, proxy, keep_alive)
    
    @property
    def driver(self):
        return self.__driver
    
    def find_element(self,by,value):
        ele = self.find_elements(by, value)
        if ele:
            return ele[0]
        else:
            logger.warn(u'[%s]element (%s) not found.' %(by,value))
            return None
                 
    # find elements
    def find_elements(self,by,value):
        if self.verify_element(by,value):
            return self.driver.find_elements(by,value)
        else:
            return []
        
    #验证元素是否存在
    def verify_element(self,by,value,times=3):
        logger.info(u'[%s]start find element:%s'%(by,value))
        ret=False
        for i in range(times):
            time.sleep(1)
            ret=self._verify_element(by, value,i==times-1)
            if ret:
                break
        return ret
    
    def _verify_element(self,by,value,islog=False):
        try:
            self.driver.find_element(by,value)
            return True
        except Exception as e:
            if islog:
                logger.warning(u'[%s]element is not found:%s\n%s' %(by,value,e))
            return False
    #向元素输入文本
    def input_text(self,by,value,text):
        ele=self.find_elements(by, value)
        if ele and len(ele)==1:
            try:
                logger.info(u'[%s]start input text (%s) to element:%s' %(by,text,value))
                ele[0].clear()
                ele[0].send_keys(text)
                return True
            except Exception as e:
                logger.error(u'[%s]input text to element (%s) fail\n%s' %(by,value,e))
                return False
        elif len(ele)>1:
            logger.warning(u'[%s]element (%s) not only one' %(by,value))
            return False
        else:
            return None
        
    #click a element
    def click_element(self,by,value):
        ele=self.find_elements(by, value)
        if ele and len(ele)==1:
            try:
                logger.info(u'[%s]start click element:%s' %(by,value))
                ele[0].click()
                return True
            except Exception as e:
                logger.error(u'[%s]click element :%s fail\n%s' %(by,value,e))
                return False
        elif len(ele)>1:
            logger.warning(u'[%s]element (%s) not only one' %(by,value))
            return False
        else:
            return None

    #get element information
    def get_element_text(self,method,para):
        ele=self.find_elements(self, method, para)
        if ele and len(ele)==1:
            try:
                logger.info(u'[%s]Start getting text information from element %s'%(method,para))
                result=ele[0].text
                return result
            except Exception as e:
                logger.error(u'[%s]getting text information from element (%s) fail \n%s' %(method,para,e))
                return None
        elif len(ele)>1:
            logger.warning(u'[%s]element (%s) not only one' %(method,para))
            return False
        else:
            return None
        
    #get attribute from element
    def get_element_attribute(self,element,att):
        logger.info(u'start get attribute from element.')
        try:
            result=element.get_attribute(att)
            logger.info(u'element attribute:%s=%s'%(att,result))
            return result
        except:
            return 0

if __name__=="__main__":
    pass