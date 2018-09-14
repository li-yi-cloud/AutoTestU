import os
import csv
import codecs
import logging
from yaml import load
import urllib3,certifi
from logging.config import dictConfigClass

from appium.webdriver import Remote 

from helper.report import PerfReport,PornographicClosureReport

from .iqueue import Iqueue,Queue
from concurrent.futures import ThreadPoolExecutor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

__config_dir = BASE_DIR + "\\config"

__log_dir = BASE_DIR + "\\logs"

logger = logging.getLogger()

def init_settings():
    global drivers
    global capabilities
    global case_list
    global user_table
    global email_sign_table
    
    with codecs.open(__config_dir+'/logging.yaml','r',"utf-8") as config_open:
        logging_config = load(config_open)
        logging_config.setdefault("version",1)
        logging_config["handlers"]["file"]["filename"]=__log_dir+"\\"+logging_config["handlers"]["file"]["filename"]
        dictConfigClass(logging_config).configure()
    
    logger.debug("load config.yaml")
    with codecs.open(__config_dir + '/config.yaml','r','utf-8') as cfp:
        config = load(cfp)
        config.setdefault("version",1)
        capabilities = config["devices"]
        case_list = config["case_list"]
    
    logger.debug("load emailsigntable.csv file")
    csv.register_dialect('idialect',delimiter='|', quoting=csv.QUOTE_ALL)  
    with codecs.open(__config_dir + '/emailsigntable.csv', 'r', 'utf-8') as efp:
        ret = csv.reader(efp,dialect='idialect')
        email_sign_table = Queue()
        for i in ret:
            if not i[0].startswith("#"):
                email_sign_table.put(i)
#         email_sign_table = Iqueue([i for i in ret if not i[0].startswith("#")])
    
    logger.debug("load usertable.csv file")
    with codecs.open(__config_dir + '/usertable.csv', 'r', 'utf-8') as ufp:
        ret = csv.reader(ufp,dialect='idialect')
        user_table = Queue()
        for i in ret:
            if not i[0].startswith("#"):
                user_table.put(i)
#         user_table = Iqueue([i for i in ret if not i[0].startswith("#")])

    logger.debug("init drivers...")
    drivers = []
    for capabilitie in capabilities:
        driver = Remote("http://127.0.0.1:4723/wd/hub",desired_capabilities=capabilitie)
        driver.implicitly_wait(0.001)
        drivers.append(driver)

def get_drivers():
    return drivers

def get_capabilities():
    return capabilities

def get_case_list():
    return case_list

def get_email_sign_table():
    return email_sign_table

def get_user_table():
    return user_table

http_client = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

perf_report = PerfReport()
closure_report = PornographicClosureReport()

thread_pool = ThreadPoolExecutor(max_workers=3)
match_time_seconds = 600

# server = "http://173.255.197.182"
server = "https://lcpic2.rcplatformhk.com"
# server = "http://39.107.25.202"
#

if __name__ == "__main__":
    pass