
import inspect
import logging
import settings
from datetime import datetime
import json,time,csv,codecs
from .iexception import RunActionFailError


logger = logging.getLogger()

def read_csv(filename):
    result = None
    try:
        result = csv.reader(codecs.open(filename, mode='r', encoding="utf-8"))
    except Exception as e:
        logger.error("read csv file \"%s\" error. reason:%s"%(filename,e))
    return result

def get_string_time():
    return time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())

def get_file_value(filename):
    try:
        with open(filename,'r') as fp:
            values=fp.read()
        return values
    except Exception as e:
        print("read file '%s' error.reason: %s"%(filename,e))
        return None

def readJson(filename):
    try:
        return json.loads(get_file_value(filename))
    except:
        return {}

def get_case_name():
    return inspect.stack()[2][3]

class ScreenShot():
    '''screen shot impelements '''
    def __init__(self,driver):
        self.driver = driver#settings.get_driver()
        self.name = ""
    
    def __call__(self):
        self.name = get_string_time() + '+' + inspect.stack()[2][3] + ".png"
        try:
            self.driver.get_screenshot_as_file(self.name)
        except Exception as e:
            logger.error("take screen shot fail. reason:\n%s"%e)

# screen_capturor = ScreenCapturor(settings.get_driver())

def ActionResult(result,message):
    logger.info('+'*40)
    casename = inspect.stack()[2][3]
    if result:
        logger.info('[Run %s success ]%s'%(casename,message))
        logger.info('+'*40)
    else:
        logger.error('[Run %s Fail ]%s'%(casename,message))
        logger.info('+'*40)
        raise RunActionFailError(casename)

if __name__ == "__main__":
    pass