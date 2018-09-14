from cases import sign,match
import time

'''
data = {
    "login_email":{
        "email":"link8@adc.com",
        "passwd":"12345678"
        },
    "match_perf":{
        "match_time_seconds": 60,
        "match_gender":"male",
        "match_location": "all",
        "report": {
            "Account": "link8@adc.com",
            "Identity": "normal free male",
            "RequestTimes": 0,
            "MatchResult": 0,
            "VideoResult": 0,
            "SpacingTime": 0
            }
        }
    }
'''

def match_perf_test(driver,data):
    driver.reset()
    time.sleep(8)
    sign.login_with_email(driver,data["login_email"])
    sign.new_user_guide_check(driver)
#     sign.new_user_popup_handle(driver)
    match.match_performance(driver, data["match_perf"])
    sign.logout_account(driver)
    driver.close_app()

'''
data={
    "email":"link8@adc.com",
    "passwd":"12345678"
    }
'''
def login_with_email(driver,data):
    driver.reset()
    time.sleep(8)
    sign.login_with_email(driver,data)
#     sign.new_user_guide_check(driver)
    driver.close_app()

'''
data={
    "email":"link8@adc.com",
    "passwd":"12345678",
    "name":"link8",
    "gender":"male"
    }
'''
def register_with_email(driver,data):
    driver.reset()
    time.sleep(8)
    sign.signup_with_email(driver, data)
#     sign.new_user_guide_check(driver)
    driver.close_app()

'''
data={
    "email":"link8@adc.com",
    "passwd":"12345678"
    }
'''
def logout_with_email(driver,data):
    driver.reset()
    time.sleep(8)
    sign.login_with_email(driver,data)
#     sign.new_user_guide_check(driver)
    sign.logout_account(driver)
    driver.close_app()

def match__(driver):
    pass

'''
data={
    "email":"link8@adc.com",
    "passwd":"12345678"
    }
'''
def new_user_popup_test(driver,data):
    driver.reset()
    time.sleep(8)
    sign.login_with_email(driver,data)
    sign.new_user_popup_test(driver)
    driver.close_app()


if __name__=="__main__":
    pass