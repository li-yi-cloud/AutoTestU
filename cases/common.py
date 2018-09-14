'''
Created on 2018年7月24日

@author: cloud
'''
import logging
from helper import elements

logger = logging.getLogger()

def restart_app(driver):
    logger.info("restart app")
    driver.close_app()
    driver.launch_app()
    for _ in range(6):
        skipfirstbutton = elements.SkipFirstButton(driver)
        if skipfirstbutton:
            try:
                skipfirstbutton.click()
            except Exception as e:
                logger.warn("click element fail. reason: %s"%e)
            finally:
                break
        elif elements.MatchHomeButton(driver) or \
                elements.NewUserGiftPopupPurchaseClose(driver) or \
                elements.GenderFilterPopupClose(driver) or \
                elements.NewUserGiftPopupRatingBar(driver) or\
                elements.SignWithFacebook(driver):
            break
        
def reset_app(driver):
    logger.info("reset app")
    driver.reset()
    for _ in range(6):
        skipfirstbutton = elements.SkipFirstButton(driver)
        if skipfirstbutton:
            try:
                skipfirstbutton.click()
            except Exception as e:
                logger.warn("click element fail. reason: %s"%e)
        if elements.SignWithFacebook(driver):
            break
def always_allow(driver):
    for _ in range(5):
        per_ele = elements.PermissionAllowButton(driver)
        if per_ele:
            per_ele.click()
if __name__=="__main__":
    pass