'''
Created on 2018年8月8日

@author: cloud
'''
import logging
from threading import Lock
from queue import Queue
# from multiprocessing import Queue

logger = logging.getLogger()

class Iqueue():
    def __init__(self,data):
        self.__lock = Lock()
        if isinstance(data, list):
            self.data = data
        else:
            raise TypeError("data must be a list type")
        self.tem_data = []
        
    def get(self):
        self.__lock.acquire()
        if len(self.data)>0:
            ret = self.data.pop(-1)
            self.tem_data.append(ret)
        else:
            logger.warn("current queue is empty !!!,will return None ")
            ret = None
        self.__lock.release()
        
        return ret
    
    def put(self,ele):
        self.__lock.acquire()
        self.data.insert(0,ele)
        self.__lock.release()
    
    def recovery(self):
        self.__lock.acquire()
        self.data = self.tem_data + self.data
        self.tem_data = []
        self.__lock.release()

if __name__ == "__main__":
    que = Queue(100)
    que.put("22")
    print(que.get())
    print(que.empty())