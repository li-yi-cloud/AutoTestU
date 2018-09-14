'''
Created on 2018年7月18日

@author: cloud
'''
import logging

logger = logging.getLogger()

class LinkAction(object):
    '''
    implement actcasesecutor  
    '''
    def __init__(self, driver):
        '''
        Constructor
        '''
        self.staus = True
        self.__driver = driver
        
    
if __name__=="__main__":
    pass