'''
Created on 2018年7月16日

@author: cloud
'''
import time
import yaml
import logging
import settings
from queue import Queue
from threading import Thread,Lock
from cases import match,sign,common
from settings.template import match_perf,match_perf_report,login_email,sign_email
from concurrent.futures import ThreadPoolExecutor,wait

logger = logging.getLogger()

class Executor():
    '''run case'''
    def __init__(self):
        settings.init_settings()
        time.sleep(5)
        self.drivers = settings.get_drivers()
        self.case_list = settings.get_case_list()
        self.login_users = settings.get_user_table()
        self.sign_users = settings.get_email_sign_table()
#         self.lock = Lock()
        self.driver_queue = Queue()
        self.thread_pool = ThreadPoolExecutor(max_workers=len(self.drivers))
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #====================================================================
    #    test action
    #====================================================================
    def restart_app(self,driver):
        common.restart_app(driver)
        time.sleep(8)
    
    def allow_permission(self,driver):
        common.always_allow(driver)
    
    def reset_app(self,driver):
        common.reset_app(driver)
        time.sleep(8)
    
    def sign_with_email(self,driver,data):
        sign.signup_with_email(driver, data)
    
    def login_with_email(self,driver,data):
        sign.login_with_email(driver, data)
    
    def new_user_guide_check(self,driver):
        sign.new_user_guide_check(driver)
    
    def logout_account(self,driver):
        sign.logout_account(driver)
    
    def new_user_popup_test(self,driver):
        sign.new_user_popup_test(driver)
    
    def delete_account(self,driver):
        sign.delete_account(driver)
    
    def new_user_popup_handle(self,driver):
        sign.new_user_popup_handle(driver)
        
    def delete_match_history(self,driver):
        match.delete_match_history(driver)
    
    def change_user_channel(self,driver,data):
        sign.change_user_channel(*data)
        
    def match_from_match_history(self,driver):
        match.match_from_match_history(driver)
        
    def match_history_report(self,driver):
        match.match_history_report(driver)
    
    def match_history_sendmessage(self,driver):
        match.match_history_sendmessage(driver)
        
    def match_history_switch(self,driver):
        match.match_history_switch(driver)
    
    def match_friend(self,driver):
        match.match_friend(driver)
        
    def match_performance(self,driver,data):
        match.match_performance(driver, data)
    
    def pornographic_closure_test(self,driver,data):
        match.pornographic_closure_test(driver,data)
    
    def pornographic_closure(self,driver,data):
        match.pornographic_closure(driver, data)
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #====================================================================
    #    generate configuration function
    #====================================================================
    def login_with_email_config(self,user):
        return yaml.load(login_email.render(email=user[0],passwd=user[1]))
    
    def sign_with_email_config(self,user):
        user = self.sign_users.get()
        return yaml.load(sign_email.render(email=user[0],passwd=user[1],gender=user[2],name=user[3]))
    
    def change_user_channel_config(self,user):
        return user[2],user[5]
    
    def match_performance_config(self,user):
        match_arg = yaml.load(match_perf.render(
                            match_time_seconds = settings.match_time_seconds
                        )
                    )
        match_arg["report"] = yaml.load(match_perf_report.render(
                                Gender = user[6],
                                Region = user[7],
                                Account = user[0],
                                UserID = user[2],
                                Identity = user[4]
                                )
                            )
        return match_arg
    
    def pornographic_closure_test_config(self,user):
        return self.match_performance_config(user)
    
    def pornographic_closure_config(self,user):
        return self.match_performance_config(user)
    #====================================================================
    #    test execution function
    #====================================================================
    def new_task(self,driver):
        logger.info("start run new_task")
        while True:
            if self.login_users.qsize() == 0:
                break
            user = self.login_users.get()
            for case in self.case_list:
                self.run_case(driver,user,case)
                
    def task(self):
        logger.info("start run task")
        driver = self.driver_queue.get()
        user = self.login_users.get()
        
        for case in self.case_list:
            self.run_case(driver,user,case)
            
        self.driver_queue.put(driver)
#         self.login_users.put(user)

    def run_case(self,driver,user,case):
        logger.info("start run case [%s]"%list(case.keys())[0])
        result = False
        for action_name in list(case.values())[0]:
            logger.info("start run action [%s]"%action_name)
            if hasattr(self, action_name):
                try:
                    if hasattr(self, "%s_config"%action_name):
                        data = getattr(self,"%s_config"%action_name)(user)
                        logger.info(str(data))
                        getattr(self,action_name)(driver,data)
                    else:
                        getattr(self,action_name)(driver)
                    result = True
                except Exception as e:
                    logger.error("run action error.reason: %s"%e)
                    result = False
                    break
        return result
    
    def execute(self):
        task_list = []
        for driver in self.drivers:
            tk = Thread(target=self.new_task,args=(driver,))
            task_list.append(tk)
            tk.start()

        for tk in task_list:
            tk.join()
    
    def start(self):
        logger.info("add driver to queue")
        for driver in self.drivers:
            self.driver_queue.put(driver)
        
        logger.info("add task to thread pool")
        task_list = {}
        for key in range(self.driver_queue.qsize()): 
            task_list[key] = self.thread_pool.submit(self.task)
            
        while True:
            if self.login_users.qsize() == 0 and False not in [task_list[key].done() for key in task_list]:
                break
            if self.driver_queue.qsize() == 0:
                logger.info("driver is busy ,sleep 5s")
                time.sleep(5)
            for key in task_list:
                if task_list[key].done():
                    task_list[key] = self.thread_pool.submit(self.task)
            
if __name__ == "__main__":
    executor = Executor()
    executor.execute()
    settings.closure_report.save_to_excel("logs/closure-%s.xlsx"%int(time.time()))
#     settings.perf_report.save_to_excel("logs/perfreport-%s.xlsx"%int(time.time()))
