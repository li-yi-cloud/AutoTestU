'''
Created on 2018年7月20日

@author: cloud
'''
from helper import elements
import time,logging
import settings
import unittest
import cases
from cases import match
from concurrent.futures import ThreadPoolExecutor,wait
from threading import Thread

logger = logging.getLogger()
settings.init_settings()
drivers = settings.get_drivers()
time.sleep(3)
driver = drivers[0]
data = {}
# elements.GenderFilterMatchButton(driver).click()
# time.sleep(2)
# driver.find_elements_by_android_uiautomator("new UiSelector().text(\"Purchase\")")
# a=driver.find_element_by_id("com.videochat.livu:id/view_title").find_element_by_xpath("android.widget.TextView[@text='Purchase']")
# print(a)
# print(elements.RechargeButton(driver).element.text)
# elements.RechargeButton(driver).click()
# driver.back()
# driver.back()
# driver.back()
# elements.MatchHistoryButton(driver).click()
# time.sleep(2)
# elements.MatchHistoryBackButton(driver).click()
# time.sleep(10)
# driver.close_app()
elements.SignWithPhone(driver).click()
time.sleep(1)
driver.find_element_by_id("com.videochat.livu:id/com_accountkit_country_code_image").click()
# print(len(driver.find_elements_by_id("com.videochat.livu:id/country_code")))


listview = driver.find_element_by_id("android:id/select_dialog_listview")
ele_point = listview.location
ele_size = listview.size

ret = True
max_times = 100
fele_text=driver.find_elements_by_id("com.videochat.livu:id/country_code")[0].text

up_move=(ele_point["x"]+ele_size['width']//2,ele_point["y"], ele_point["x"]+ele_size['width']//2, ele_point["y"]+ele_size['height'], 2200)
down_move=(ele_point["x"]+ele_size['width']//2, ele_point["y"]+ele_size['height'], ele_point["x"]+ele_size['width']//2,ele_point["y"], 2200)
print(up_move)
print(down_move)
# for i in range(max_times):
#     driver.swipe(*up_move)
#     cur_ele_text = driver.find_elements_by_id("com.videochat.livu:id/country_code")[0].text
#     print("fele: [%s] curele: [%s]"%(fele_text,cur_ele_text))
#     if cur_ele_text == fele_text:
#         break
#     else:
#         fele_text = cur_ele_text
# 
# print("+"*20)
while ret:    
    for ele in driver.find_elements_by_id("com.videochat.livu:id/country_code"):
        print(ele.text)
        if ele.text == "+86":
            ret = False
            break
    if ret and max_times >0:
        driver.swipe(*up_move)
    max_times-=1
    if max_times == 0:
        break

# driver.start_activity(capabilities["appPackage"], capabilities["appActivity"])
time.sleep(20)
driver.close_app()


class Executor(unittest.TestCase):
    def setUp(self):
        self.drivers = settings.get_drivers()
        self.__conf = None
    
    def match_performance(self):
        match.match_performance(driver, data)
        
    def confAnalysis(self):
        pass 
    
    def task(self,case,*args,**kwargs):
        try:
            case(*args,**kwargs)
        except Exception as e:
            logger.error("run task [%s] error. \nreason: %s"%(case.__name__,e))
            
    def run(self):
        tasks = []
        task_args = [driver,data]
        work_thread_pool = ThreadPoolExecutor(len(drivers))
        task = cases.match_perf_test
        for task_arg in task_args:
            tasks.append(work_thread_pool.submit(task,task_arg))
        wait(tasks)
        cases.match_perf_test(driver, data)
        settings.perf_report.to_dataframe.to_csv("logs/perfreport.csv")

data={}
thread_list=[]
for index,driver in enumerate(drivers):
    th = Thread(target=cases.match_perf_test,args=(driver, data[index]))
    thread_list.append(th)
    th.start()

for th in thread_list:
    th.join()
    
settings.perf_report.to_dataframe.to_csv("logs/perfreport.csv")
