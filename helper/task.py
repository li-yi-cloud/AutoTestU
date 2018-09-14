'''
Created on 2018年7月30日

@author: cloud
'''
import time,random
import yaml
import logging
import settings
from functools import reduce
from threading import Thread,Lock
from cases import match,sign,common

logger = logging.getLogger()

class Task():
    '''
    document of task
    work_method:
    args : work_method's args. 
    '''
    def __init__(self,work_method,para):
        self.__work = work_method
        self.__para = para
        
    def run(self,*args,**kwargs):
        logger.info("start run work: [%s]"%self.__work.__name__)
        ret = False
        try:
            self.__work(*args,**kwargs)
            ret = True
        except Exception as e:
            logger.error("run work [%s] fail,reason %s"%(self.__work.__name__,e))
        return ret
    def __call__(self):
        if isinstance(self.__para, dict):
            return self.run(**self.__para)
        elif isinstance(self.__para, tuple):
            return self.run(*self.__para)
        else:
            return False
            logger.warning("invalid type of para")
            
# time.sleep(8)
def random_generate_user():
    pass

def generate_users_with_random(drivers):
    user_table = settings.get_user_table()
    users = []
    if len(user_table)<len(drivers):
        from helper.iexception import LengthError
        raise LengthError("user is not enough in user table.")
    while len(users)<len(drivers):
        user = random.choice(user_table)
        if user not in users:
            users.append(user)
        else:
            logger.info("user is repeated")
    return users

def generate_users(drivers):
    user_table = settings.get_user_table()
    drivers_length = len(drivers)
    if len(user_table)<len(drivers):
        from helper.iexception import LengthError
        raise LengthError("user is not enough in user table.")
    return [reduce(lambda x,y: (x[0],x[1]+y[1]),filter(lambda x:x[0]==driver_id,map(lambda user: (user[0]%drivers_length,[user[1]]) ,enumerate(user_table)))) for driver_id in range(drivers_length)]
    
def create_match_perf_config(user):
    from settings.template import match_perf
    
    return yaml.load(match_perf.render(
                        match_time_seconds = settings.match_time_seconds,\
                        gender = user[4],
                        location = user[5],
                        Account = user[0],
                        Identity = user[3]
                        )
                    )

def create_login_config(user):
    from settings.template import login_email
    
    return yaml.load(login_email.render(email=user[0],passwd=user[1]))

# settings.init_settings()
# drivers = settings.get_drivers()
# 
# print(generate_users(drivers))
# print(create_login_config(genarate_users(drivers)[0][1][0]))
# print(create_match_perf_config(genarate_users(drivers)[0][1][1]))

# import os
# os._exit(1)
class Executor():
    '''run case'''
    def __init__(self):
        settings.init_settings()
        time.sleep(5)
        self.drivers = settings.get_drivers()
        self.case_list = settings.get_case_list()
        self.drivers_users = generate_users(self.drivers)
        self.lock = Lock()
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #====================================================================
    #    test action
    #====================================================================
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
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #====================================================================
    #    generate configuration function
    #====================================================================
    def login_with_email_config(self,user):
        return create_login_config(user)
    
    def sign_with_email_config(self,user):
        return random_generate_user()
    
    def match_performance_config(self,user):
        return create_match_perf_config(user)
        
    #====================================================================
    #    test execution function
    #====================================================================
    def task(self,driver,users):
        logger.info("start run task")
        for user in users:
            self._task(driver,user)

    def _task(self,driver,user):
        logger.info("start run _task")
        for case_name in sorted(self.case_list.keys()):
            self.run_case(driver, user, case_name)
    
    def run_case(self,driver,user,case_name):
        logger.info("start run case [%s]"%case_name)
        result = False
        for action_name in self.case_list[case_name]:
            logger.info("start run action [%s]"%action_name)
            if hasattr(self, action_name):
                try:
                    if hasattr(self, "%s_config"%action_name):
                        data = getattr(self,"%s_config"%action_name)(user)
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
        for index,driver in enumerate(self.drivers):
            tk = Thread(target=self.task,args=(driver,self.drivers_users[index][1]))
            task_list.append(tk)
            tk.start()

        for tk in task_list:
            tk.join()
                
executor = Executor()
executor.execute()
if __name__=="__main__":
    pass