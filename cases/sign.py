'''
Created on 2018年7月20日

@author: cloud
'''
import time,logging
from helper import elements
from helper import ActionResult
from cases.common import restart_app
import settings

logger = logging.getLogger()

def signup_with_email(driver,data):
    elements.MoreOptions(driver).click()
    time.sleep(1)
    elements.SignWithEmail(driver).click()
    elements.SignEmailInput(driver).input_text(data["email"])
    pwdinput = elements.SignPasswdInput(driver)
    pwdinput.input_text(data["passwd"])
#     driver.back()
    elements.SignWithEmailNextButton(driver).click()
    elements.SignNameSettingInput(driver).input_text(data["name"])
    elements.SignBirthdayInput(driver).click()
    elements.SignBirthdayInputDone(driver).click()
    if data["gender"] == "male":
        elements.SignMaleCheckbox(driver).click()
    else:
        elements.SignFemaleCheckbox(driver).click()
    elements.SignConfirm(driver).click()

    ret = False
    if elements.MatchHomeButton(driver) or \
            elements.GenderFilterPopupClose(driver) or \
            elements.NewUserGiftPopupPurchase(driver) or \
            elements.NewUserGiftPopupRatingBar(driver):
        ret = True
    
    return ActionResult(ret,"sign with email")

def login_with_email(driver,data):
    elements.MoreOptions(driver).click()
    elements.LoginWithEmail(driver).click()
    elements.SignEmailInput(driver).input_text(data["email"])
    elements.SignPasswdInput(driver).input_text(data["passwd"])
#     driver.back()
    elements.LoginWithEmailConfirm(driver).click()
    
    time.sleep(3)
    ret = False
    if elements.MatchHomeButton(driver) or \
            elements.GenderFilterPopupClose(driver) or \
            elements.NewUserGiftPopupPurchase(driver) or \
            elements.NewUserGiftPopupRatingBar(driver)or\
            elements.NewUserGuideClose(driver) or\
            elements.PermissionAllowButton(driver):
        ret = True
        
    return ActionResult(ret,"login with email")

def logout_account(driver):
    elements.UserHomeButton(driver).click()
    elements.UserSetting(driver).click()
    elements.UserSettingLogout(driver).click()
    elements.EnsureButton(driver).click()
    
    return ActionResult(bool(elements.SignWithFacebook(driver)),"logout account")

def delete_account(driver):
    elements.UserHomeButton(driver).click()
    elements.UserSetting(driver).click()
    ele = elements.UserSettingPageBody(driver)
    ele_loction = ele.location
    ele_size = ele.size
    driver.swipe(ele_loction["x"]+ele_size["width"]//2,ele_loction["y"]+ele_size['height']\
                 ,ele_loction["x"]+ele_size["width"]//2,ele_loction["y"],500)
    
    if elements.UserSettingDeleteAccountButton(driver):
        elements.UserSettingDeleteAccountButton(driver).click()
        if elements.DeleteAccountReasonPage(driver):
            elements.DeleteAccountReasonHowToUse(driver).click()
            elements.DeleteAccountConfirm(driver).click()
            elements.DeleteAccountUnderstandExplanationCheckbox(driver).click()
            elements.DeleteAccountConfirm(driver).click()
            elements.EnsureButton(driver).click()
    
    ret = elements.SignWithFacebook(driver)
    
    return ActionResult(ret,"delete account")

def new_user_guide_check(driver):
    time.sleep(2)
    ret = False
    if elements.NewUserGuideClose(driver):
        elements.NewUserGuideClose(driver).click()
        elements.NewUserGuideMatchTips(driver).click()
        driver.back()
        elements.MatchStopEnsureButton(driver,2,0.2).click()
        
        ret = True
    else:
        ret = elements.MatchHomeButton(driver)
    time.sleep(3)
    return ActionResult(ret,"new user guide check")

def new_user_popup_handle(driver):
    for _ in range(2):
        if elements.MatchHomeButton(driver):
            break
        if elements.NewUserGiftPopupPurchase(driver):
            elements.NewUserGiftPopupPurchaseClose(driver).click()
        elif elements.NewUserGiftPopupRatingBar(driver):
            elements.NewUserGiftPopupRatingBar(driver).click()
            elements.NewUserGiftPopupRatingCancel(driver).click()
        elif elements.GenderFilterPopupClose(driver):
            elements.GenderFilterPopupClose(driver).click()

    return ActionResult(elements.MatchHomeButton(driver), "new user popup handle")

def new_user_popup_test(driver):
#     signup_with_email(driver,data)
#     new_user_guide_check(driver)
    popup_result = []
    for i in range(1,101):
        restart_app(driver)
        time.sleep(3)
        if elements.MatchHomeButton(driver):
            logger.info("no popup element")
            continue
        for _ in range(3):
            no_popup = False
            for ele_class in [elements.NewUserGiftPopupPurchase,elements.NewUserGiftPopupRatingBar,elements.GenderFilterPopupClose]:
                ele_instance = ele_class(driver)
                if ele_instance:
                    logger.info("[%d] --> (%s)"%(i,ele_class(driver).ele_name))
                    popup_result.append((i,ele_class(driver).ele_name))
                    # close Popup
                    if isinstance(ele_instance, elements.NewUserGiftPopupPurchase):
                        elements.NewUserGiftPopupPurchaseClose(driver).click()
                    elif isinstance(ele_instance, elements.NewUserGiftPopupRatingBar):
                        elements.NewUserGiftPopupRatingBar(driver).click()
                        elements.NewUserGiftPopupRatingCancel(driver).click()
                    elif isinstance(ele_instance, elements.GenderFilterPopupClose):
                        elements.GenderFilterPopupClose(driver).click()
                no_popup = elements.MatchHomeButton(driver)
                if no_popup:
                    break
            if no_popup:
                break
#                 logger.info("no popup element")
    logger.info(str(popup_result))
    return ActionResult(True, "new user popup test")

def change_user_channel(userid,userchannel):
    channelmap = {
        "默认":0,
        "自然渠道":1,
        "install":2,
        "AEO or InApp":3
        }
    
    if userchannel not in channelmap:
        logger.warning("invalid user channel [%s],will use default."%userchannel)
    
    data = {
        "userId":userid,
        "channelId":channelmap[userchannel] if userchannel in channelmap else 0
        }
    req = settings.http_client.request("POST",settings.template.update_channel_url.render(server=settings.server),fields=data)
    
    return ActionResult(req.status == 200, "change user channel [%s]"%req.status)
    
if __name__ == "__main__":
    change_user_channel("7793367", "默认")
#     pass
    

    
    