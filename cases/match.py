'''
Created on 2018年7月23日

@author: cloud
'''
import time,logging
from helper import elements
from helper import ActionResult
import settings
from datetime import datetime
import copy,re
from . import common,sign

logger = logging.getLogger()

def match_history_report(driver):
    elements.MatchHistoryButton(driver).click()
    if elements.MatchHistoryStartMatchButton(driver):
        match_from_match_history(driver)
        elements.MatchHistoryButton(driver).click()
    match_time = elements.MatchHistoryMatchTime(driver).text
    elements.MatchHistoryCardReportButton(driver).click()
    elements.MatchHistoryReportFakeGender(driver).click()
    
    return ActionResult(match_time != elements.MatchHistoryMatchTime(driver).text, "report from match history")

def match_from_match_history(driver):
    elements.MatchHistoryStartMatchButton(driver).click()
    friends_list = []
    ctime = time.time()
    while time.time() < (ctime+600):
        match_popup_handle(driver)
        if elements.VideoingObjectUserName(driver):
            logger.info("match success.")
            logger.info("UserName: %s,UserFavoriteNumber: %s,UserLocation: %s"%(elements.VideoingObjectUserName(driver).text,\
                                                                                elements.VideoingObjectFavoriteNumber(driver).text,\
                                                                                elements.VideoingObjectLocation(driver).text))
            friends_list.append(elements.VideoingObjectUserName(driver).text)
            time.sleep(10)
            # quit current match
            elements.VideoingQuit(driver).click()
            
        if len(friends_list) >= 10:
            break
    if not elements.MatchHistoryButton(driver):
        driver.back()
        elements.MatchStopEnsureButton(driver).click()
    
    ret = elements.MatchHistoryButton(driver)
    
    return ActionResult(ret,"match friends if match history page is empty")

def delete_match_history(driver):
    elements.MatchHistoryButton(driver).click()
    if elements.MatchHistoryStartMatchButton(driver):
        match_from_match_history(driver)
        elements.MatchHistoryButton(driver).click()
    if elements.MatchHistoryStartMatchButton(driver):
        return ActionResult(False, "delete a match history - Match history is empty")
    
    match_time = elements.MatchHistoryMatchTime(driver).text
    for _ in range(3):
        if elements.MatchHistoryMatchTime(driver):
            elements.MatchHistoryCardDeleteButton(driver).click()
            elements.EnsureButton(driver).click()
        else:
            break
    
    ret = False
    if elements.MatchHistoryMatchTime(driver):
        ret = match_time != elements.MatchHistoryMatchTime(driver).text
    elif elements.MatchHistoryStartMatchButton(driver):
        ret = True
    return ActionResult(ret, "delete a match history")

def match_history_switch(driver):
    elements.MatchHistoryButton(driver).click()
    if elements.MatchHistoryStartMatchButton(driver):
        match_from_match_history(driver)
        elements.MatchHistoryButton(driver).click()
    head_ele = elements.MatchHistoryUserHeadImage(driver).element
    if head_ele:
        ele_point = head_ele.location
        ele_size = head_ele.size
        right_move_point = (ele_point['x']+ele_size['width'],ele_point['y']+ele_size['height']//2,ele_point['x'],ele_point['y']+ele_size['height']//2,500)
        left_move_point = (ele_point['x'],ele_point['y']+ele_size['height']//2,ele_point['x']+ele_size['width'],ele_point['y']+ele_size['height']//2,500)
        match_time = elements.MatchHistoryMatchTime(driver).text
        driver.swipe(*right_move_point)
        ret = match_time != elements.MatchHistoryMatchTime(driver).text
        if ret :
            driver.swipe(*left_move_point)
            ret = match_time == elements.MatchHistoryMatchTime(driver).text
        return ActionResult(ret,"test left and right swipe screen")
    else:
        return ActionResult(False,"test left and right swipe screen")
    
def match_history_sendmessage(driver):
    elements.MatchHistoryButton(driver).click()
    if elements.MatchHistoryStartMatchButton(driver):
        match_from_match_history(driver)
        elements.MatchHistoryButton(driver).click()
    elements.MatchHistoryCardSendMessaeButton(driver).click()
    ret = False
    # don't have enough coins
    if elements.MatchHistorySendMessageSpendCoinsTips(driver):
        elements.CancelButton(driver).click()
        ret = True
    # have enough coins
    elif elements.MessageFriendsChatInput(driver):
        ret = True
    else:
        ret = False
    return ActionResult(ret,"send message from match history")

def match_friend(driver):
    if not elements.MatchHistoryButton(driver):
        elements.MatchHomeButton(driver).click()
    #start match
    elements.MatchHomeButton(driver).click()
    friends_list = []
    ctime = time.time()
    while time.time() < (ctime+600):
        match_popup_handle(driver)
        if elements.VideoingObjectUserName(driver):
            logger.info("match success.")
            logger.info("UserName: %s,UserFavoriteNumber: %s,UserLocation: %s"%(elements.VideoingObjectUserName(driver).text,\
                                                                                elements.VideoingObjectFavoriteNumber(driver).text,\
                                                                                elements.VideoingObjectLocation(driver).text))
            friends_list.append(elements.VideoingObjectUserName(driver).text)
            time.sleep(10)
            # quit current match
            elements.VideoingQuit(driver).click()
            
        if len(friends_list) >= 10:
            break
    if not elements.MatchHistoryButton(driver):
        driver.back()
        elements.MatchStopEnsureButton(driver).click()
    
    ret = elements.MatchHistoryButton(driver)
    
    return ActionResult(ret,"match friends")

def match_popup_handle(driver):
    if elements.MatchingGenderFilterPopupClose(driver):
        elements.MatchingGenderFilterPopupClose(driver).click()
    elif elements.NewUserGiftPopupPurchase(driver):
        elements.NewUserGiftPopUpPurchaseSkip(driver).click()

def verify_match_history(driver):
    elements.MatchHistoryButton(driver).click()
    if elements.MatchHistoryStartMatchButton(driver):
        match_from_match_history(driver)
        elements.MatchHistoryButton(driver).click()
    logger.info("name: %s ,favorite: %s ,location: %s ,time: %s"%(elements.MatchHistoryUserName(driver).text,\
                                                       elements.MatchHistoryUserPraiseCount(driver).text,\
                                                       elements.MatchHistoryUserLocation(driver).text,\
                                                       elements.MatchHistoryMatchTime(driver).text))
    
    return ActionResult(elements.MatchHistoryUserHeadImage(driver), "verify match history user information")

'''
data = {
    "match_time_seconds": 1800,
    "report": {
        "Time":"",
        "Account": "link8@adc.com",
        "Identity": "normal free male",
        "RequestTimes": 0,
        "MatchResult": 0,
        "VideoResult": 0,
        "SpacingTime": 0
        }
    }

'''
def match_performance(driver,data):
    if not elements.UserHomeButton(driver):
        elements.MatchHomeButton(driver).click()
    match_gender_filter(driver, data)
    match_region_filter(driver, data)
    #start match
    elements.MatchHomeButton(driver).click()
    start_time = float(time.mktime(time.strptime(driver.device_time,'%a %b %d %H:%M:%S CST %Y')))
    current_time = time.time()
    while time.time() < (current_time+data["match_time_seconds"]):
        ret = copy.deepcopy(data["report"])
        vstime = time.time()
        if elements.VideoingQuit(driver,1):
            vtime = time.time() - vstime 
            start_time += vtime
            logger.info("connect success,start time (%s)"%start_time)
            ret["MatchResult"] = 1
            ret["VideoResult"] = 1
            c_time = time.mktime(time.strptime(driver.device_time,'%a %b %d %H:%M:%S CST %Y'))
            match_info = ""
            for _ in range(2):
                match_info = elements.MatchInfoElement(driver,1).text
                if match_info:
                    break
            if match_info:
                reqtimes,matcheduid,match_time = match_info.split("|")
                ret["RequestTimes"] = int(reqtimes) if re.match(r'^\d{1,}$', reqtimes) else None
                ret["MatchedUserID"] = int(matcheduid) if re.match(r'^\d{1,}$', matcheduid) else None
                faild_video_ele = elements.MatchVideoErrorInfoElement(driver,1)
                if not faild_video_ele:
                    ret["MatchSpacingTime"] = (int(match_time)/1000 - start_time) if (int(match_time)/1000 - start_time) > 0 else 1.0
                    ret["VideoSpacingTime"] = (c_time - start_time) if (c_time - start_time) > 0 else 1.1
                else:
                    fail_video_text = ""
                    for _ in range(2):
                        fail_video_text = elements.MatchVideoErrorInfoElement(driver,1).text
                        if fail_video_text:
                            break
                    if fail_video_text:
                        _start_time = int(fail_video_text.split(",")[-1].split("|")[-1])/1000 + vtime
                        ret["MatchSpacingTime"] = (int(match_time)/1000 - _start_time) if (int(match_time)/1000 - _start_time) > 0 else 1.0
                        ret["VideoSpacingTime"] = (c_time - _start_time) if (c_time - _start_time) > 0 else 1.1
                        
                        settings.thread_pool.submit(put_connect_fail,data, fail_video_text, start_time)
#                         fail_job = Thread(target=put_connect_fail,args=(data, fail_video_text, start_time))
#                         fail_job.start()
                    else:
                        ret["MatchSpacingTime"] = (int(match_time)/1000 - start_time) if (int(match_time)/1000 - start_time) > 0 else 1.0
                        ret["VideoSpacingTime"] = (c_time - start_time) if (c_time - start_time) > 0 else 1.1
                
                settings.thread_pool.submit(settings.perf_report.append,ret,3.25)        
#                 report_job = Thread(target=settings.perf_report.append,args=(ret,2.25))
#                 report_job.start()
                
                match_video_quit(driver,data)
                start_time = float(time.mktime(time.strptime(driver.device_time,'%a %b %d %H:%M:%S CST %Y')))
    time.sleep(2)
    driver.close_app()
    return ActionResult(True,"match performance")

def put_connect_fail(data,fail_text,start_time):
    temp_start_time = start_time
    for failInfo in fail_text.split(","):
        ret = copy.deepcopy(data["report"])
        reqtimes,matcheduid,match_time = failInfo.split("|")
        ret["RequestTimes"] = int(reqtimes) if re.match(r'^\d{1,}$', reqtimes) else None
        ret["MatchedUserID"] = int(matcheduid) if re.match(r'^\d{1,}$', matcheduid) else None
        ret["MatchResult"] = 1
        ret["MatchSpacingTime"] = (int(match_time)/1000 - temp_start_time) if (int(match_time)/1000 - temp_start_time) > 0 else 1
        temp_start_time = int(match_time)/1000
        
        settings.perf_report.append(ret,3.25)

def match_video_quit(driver,data):
    times = time.time()+10
    video_quit = False
    elements.VideoingQuit(driver,2,0.5).click()
    time.sleep(0.5)
    while times>time.time():
        quit_ele = elements.VideoingQuitText(driver,1,0.5)
        if quit_ele:
            logger.info("quit video ...%s"%quit_ele.text)
            if quit_ele.text:
                time.sleep(0.5)
                continue
            else:
                break
        elif elements.MatchingTips(driver,1,0.5):
            video_quit = True
            break
        elif elements.VideoingQuit(driver,1,0.5):
            break

        
    if not video_quit:
        elements.VideoingQuit(driver,1,0.5).click()
        
def match_gender_filter(driver,data):
    if elements.GenderFilterMatchButton(driver):
        elements.GenderFilterMatchButton(driver).click()
    else:
        elements.GenderFilterMatchButtonTv(driver).click()
    if data["report"]["ClientMatchGender"] == "male":
        elements.GenderFilterMatchMaleCheckBox(driver).click()
    elif data["report"]["ClientMatchGender"] == "female":
        elements.GenderFilterMatchFemaleCheckBox(driver).click()
    elif data["report"]["ClientMatchGender"] == "all":
        elements.GenderFilterMatchAllCheckBox(driver).click()
    elif data["report"]["ClientMatchGender"] == "goddess":
        elements.GenderFilterMatchGoddessCheckBox(driver).click()
    else:
        driver.back()

def match_region_filter(driver,data):
    if elements.RegionFilterMatchButton(driver):
        elements.RegionFilterMatchButton(driver).click()
        if data["report"]["ClientMatchRegion"] != "global":
            elements.RegionFilterMatchGlobal(driver).click()
        else:
            elements.RegionFilterMatchOther(driver).click()

def take_match_result(driver,ret,start_time):
    ret["VideoSpacingTime"] = time.time() - start_time
    reqtimes = elements.MatchRequestElement(driver).text
    ret["RequestTimes"] = int(reqtimes) if re.match(r'^\d{1,}$', reqtimes) else None
    ret["ChannelID"] = elements.MatchVideoChannelIdElement(driver).text
    matcheduid = elements.MatchRemoteUserIdElement(driver).text
    ret["MatchedUserID"] = int(matcheduid) if re.match(r'^\d{1,}$', matcheduid) else None

def pornographic_closure_test(driver,data):
    report = {
            "Account":data["report"]["Account"],
            "MatchedUserID":None,
            "UserID":data["report"]["UserID"],
            "Identity":data["report"]["Identity"],
            "VideoTimes":None,
            "IsSnaphot":None,
            "IsClosure":None,
            "IsUnlock":None,
            "ClosureTime":None,
            "CoinsBeforeUnlock":None,
            "CoinsAfterUnlock":None,
            "ClosureTimes":None,
            "UnlockPrice":None,
            "DeductionResult":None
        }
    elements.UserHomeButton(driver).click()
    coin_number = int(elements.MatchPageCoinsElement(driver).text)
    elements.MatchHomeButton(driver).click()
    
    logger.info("before match coin number: %s"%coin_number)
    if elements.MatchPornographicTestCheckBox(driver).element.get_attribute("checked") == 'false':
        elements.MatchPornographicTestCheckBox(driver).click()
    
    match_gender_filter(driver, data)
    time.sleep(1)
    elements.MatchHomeButton(driver).click()
    
    end_time=time.time() + data["match_time_seconds"]
    lock_times = 0
    first_video = True
    video_times = 0
    remote_user_id = ""
    tmp_report = copy.deepcopy(report)
    while time.time() < end_time and lock_times < 4:
#         tmp_report = copy.deepcopy(report)
        if elements.VideoingQuit(driver,1):
            video_times +=1
            if first_video:
                logger.info("first video not save [%s]"%video_times)
                match_info = elements.MatchInfoElement(driver).text
                if match_info:
                    reqtimes,matcheduid,match_time = match_info.split("|")
                    tmp_report["VideoTimes"] = video_times
                    tmp_report["MatchedUserID"] = matcheduid
                    tmp_report["IsSnaphot"] = elements.MatchPornographicIsSnapshot(driver).text
                first_video = False
            else:
                logger.info("not first video save [%s]"%video_times)
                tmp_report["IsClosure"] = False
                
                settings.thread_pool.submit(settings.closure_report.append,tmp_report,3.25)
                
                tmp_report = copy.deepcopy(report)
                match_info = elements.MatchInfoElement(driver).text
                if match_info:
                    reqtimes,matcheduid,match_time = match_info.split("|")
                    tmp_report["MatchedUserID"] = matcheduid
                tmp_report["VideoTimes"] = video_times
                tmp_report["IsSnaphot"] = elements.MatchPornographicIsSnapshot(driver).text
            match_video_quit(driver, data)
            
        elif elements.MatchPornographicPopUpElement(driver):
            #closure
            tmp_report["VideoTimes"] = video_times
            tmp_report["IsClosure"] = True
            tmp_report["ClosureTimes"] = lock_times + 1
            tmp_report["ClosureTime"] = elements.MatchPornographicClosureTimeElement(driver).text
            tmp_report["IsSnaphot"] = "true"
            lock_times += 1
            if elements.MatchPornographicPopUpUnlock(driver):
                tmp_report["IsUnlock"] = True
                elements.MatchPornographicPopUpCancel(driver).click()
                elements.UserHomeButton(driver).click()
                coin_number = int(elements.MatchPageCoinsElement(driver).text)
                elements.MatchHomeButton(driver).click()
                tmp_report["CoinsBeforeUnlock"] = coin_number
                
                logger.info("Coin Number: %s"%coin_number)
                elements.MatchHomeButton(driver).click()
                
                elements.MatchPornographicPopUpUnlock(driver,6,1).click()
                unlock_price_tips = elements.MatchPornographicUnlockCoins(driver).text
                unlock_price = re.search(r'\d{1,}', unlock_price_tips).group(0) if re.search(r'\d{1,}', unlock_price_tips) else None
                logger.info(unlock_price_tips)
                
                # unlock price
                tmp_report["UnlockPrice"] = unlock_price
                
                elements.MatchPornographicPopUpUnlock(driver).click()
                time.sleep(1)
                common.restart_app(driver)
                sign.new_user_popup_handle(driver)
                
                if elements.MatchPornographicTestCheckBox(driver).element.get_attribute("checked") == 'false':
                    elements.MatchPornographicTestCheckBox(driver).click()
                
                elements.UserHomeButton(driver).click()
                temp_coin_number = int(elements.MatchPageCoinsElement(driver).text)
                elements.MatchHomeButton(driver).click()
                logger.info("current coin number: %s"%temp_coin_number)
                
                tmp_report["CoinsAfterUnlock"] = temp_coin_number
                if int(unlock_price) == coin_number - temp_coin_number:
                    tmp_report["DeductionResult"] = True
                else:
                    tmp_report["DeductionResult"] = False
                    
                coin_number = temp_coin_number
                logger.info("Coin Number: %s"%coin_number)
                elements.MatchHomeButton(driver).click()
                first_video = True
            else:
                tmp_report["IsUnlock"] = False
                elements.MatchPornographicPopUpCancel(driver).click()
                elements.MatchHomeButton(driver).click()
                elements.MatchHomeButton(driver).click()
                
                
            settings.thread_pool.submit(settings.closure_report.append,tmp_report,3.25)
            tmp_report = copy.deepcopy(report)
            
        elif elements.MatchPornographicAlert(driver):
            elements.MatchPornographicAlert(driver).click()
    
    driver.close_app()
    
def pornographic_closure(driver,data):
    report = {
            "Account":data["report"]["Account"],
            "MatchedUserID":None,
            "UserID":data["report"]["UserID"],
            "Identity":data["report"]["Identity"],
            "VideoTimes":None,
#             "IsSnapshot":None,
            "SnapshotTimes":None,
            "VideoStartTime":None,
            "FirstSnapshortTime":None,
            "LastSnapshotTime":None,
            "IsClosure":None,
            "IsUnlock":None,
            "ClosureTime":None,
            "CoinsBeforeUnlock":None,
            "CoinsAfterUnlock":None,
            "ClosureTimes":None,
            "UnlockPrice":None,
            "DeductionResult":None
        }
    elements.UserHomeButton(driver).click()
    coin_number = int(elements.MatchPageCoinsElement(driver).text)
    elements.MatchHomeButton(driver).click()
    
    logger.info("before match coin number: %s"%coin_number)
    if elements.MatchPornographicTestCheckBox(driver).element.get_attribute("checked") == 'false':
        elements.MatchPornographicTestCheckBox(driver).click()
    
    match_gender_filter(driver, data)
    time.sleep(1)
    
    
    end_time=time.time() + data["match_time_seconds"]
    lock_times = 0
    first_video = True
    video_times = 0
    remote_user_id = ""
    tmp_report = copy.deepcopy(report)
    elements.MatchHomeButton(driver).click()
    while time.time() < end_time and lock_times < 4:
        if elements.MatchInfoElement(driver):
            logger.info("video connect success.")
            video_times +=1
            
            if first_video:
                logger.info("first video not save [%s]"%video_times)
                tmp_report = pornographic_closure_report_info(driver, tmp_report)
                tmp_report["VideoTimes"] = video_times
                
                first_video = False
            else:
                logger.info("not first video save [%s]"%video_times)
                tmp_report["IsClosure"] = False
                
                settings.thread_pool.submit(settings.closure_report.append,tmp_report,3.25)
                
                tmp_report = copy.deepcopy(report)
                
                tmp_report = pornographic_closure_report_info(driver, tmp_report)
                tmp_report["VideoTimes"] = video_times
            pornographic_closure_hangup(driver, data)
        elif elements.MatchPornographicPopUpElement(driver):
            logger.info("closure with pornographic")
            tmp_report["VideoTimes"] = video_times
            tmp_report["IsClosure"] = True
            tmp_report["ClosureTimes"] = lock_times + 1
            tmp_report["ClosureTime"] = elements.MatchPornographicClosureTimeElement(driver).text
#             tmp_report["IsSnaphot"] = "true"
            lock_times += 1
            if elements.MatchPornographicPopUpUnlock(driver):
                tmp_report["IsUnlock"] = True
                elements.MatchPornographicPopUpCancel(driver).click()
                elements.UserHomeButton(driver).click()
                coin_number = int(elements.MatchPageCoinsElement(driver).text)
                elements.MatchHomeButton(driver).click()
                tmp_report["CoinsBeforeUnlock"] = coin_number
                
                logger.info("Coin Number: %s"%coin_number)
                elements.MatchHomeButton(driver).click()
                
                elements.MatchPornographicPopUpUnlock(driver,6,1).click()
                unlock_price_tips = elements.MatchPornographicUnlockCoins(driver).text
                unlock_price = re.search(r'\d{1,}', unlock_price_tips).group(0) if re.search(r'\d{1,}', unlock_price_tips) else None
                logger.info(unlock_price_tips)
                
                # unlock price
                tmp_report["UnlockPrice"] = unlock_price
                
                elements.MatchPornographicPopUpUnlock(driver).click()
                time.sleep(0.5)
                driver.back()
                time.sleep(0.2)
                elements.MatchStopEnsureButton(driver).click()
#                 common.restart_app(driver)
#                 sign.new_user_popup_handle(driver)
                
                if elements.MatchPornographicTestCheckBox(driver).element.get_attribute("checked") == 'false':
                    elements.MatchPornographicTestCheckBox(driver).click()
                
                elements.UserHomeButton(driver).click()
                temp_coin_number = int(elements.MatchPageCoinsElement(driver).text)
                elements.MatchHomeButton(driver).click()
                logger.info("current coin number: %s"%temp_coin_number)
                
                tmp_report["CoinsAfterUnlock"] = temp_coin_number
                if int(unlock_price) == coin_number - temp_coin_number:
                    tmp_report["DeductionResult"] = True
                else:
                    tmp_report["DeductionResult"] = False
                    
                coin_number = temp_coin_number
                logger.info("Coin Number: %s"%coin_number)
                elements.MatchHomeButton(driver).click()
                first_video = True
            else:
                tmp_report["IsUnlock"] = False
                elements.MatchPornographicPopUpCancel(driver).click()
                elements.MatchHomeButton(driver).click()
                elements.MatchHomeButton(driver).click()
                
                
            settings.thread_pool.submit(settings.closure_report.append,tmp_report,3.25)
            tmp_report = copy.deepcopy(report)
        elif elements.MatchPornographicAlert(driver):
            logger.info("closure alert with pornographic")
            elements.MatchPornographicAlert(driver).click()
    driver.close_app()
    
def pornographic_closure_hangup(driver,data):
    times = time.time()+10
    video_quit = False
    elements.VideoingQuit(driver,2,0.5).click()
    time.sleep(0.5)
    while times>time.time():
        quit_ele = elements.VideoingQuitText(driver,1,0.5)
        if quit_ele:
            logger.info("quit video ...%s"%quit_ele.text)
            if quit_ele.text:
                time.sleep(0.5)
                continue
            else:
                break
        elif elements.MatchingTips(driver,1,0.5):
            video_quit = True
            break
        elif elements.VideoingQuit(driver,1,0.5):
            break
        elif elements.MatchPornographicPopUpElement(driver,1):
            video_quit = True
            break

        
    if not video_quit:
        elements.VideoingQuit(driver,1,0.5).click()
       
def pornographic_closure_report_info(driver,report):
    
    report["VideoStartTime"] = datetime.fromtimestamp(time.time());
    match_info = elements.MatchInfoElement(driver).text
    if match_info:
        reqtimes,matcheduid,match_time = match_info.split("|")
        report["MatchedUserID"] = matcheduid
    sn_time = time.time()+10
    sn_times = 0
    max_space_time_second = 3
    s_time = 0
    while time.time() < sn_time:
        if elements.MatchInfoElement(driver):
            sn_times = elements.MatchVideoSnaphotTimes(driver).text
            if sn_times:
                if sn_times == "1":
                    report["FirstSnapshortTime"] = datetime.now()
                    report["SnapshotTimes"]=sn_times;
                    s_time = time.time()
                    while time.time()<s_time+max_space_time_second:
                        tmp_sn_times = elements.MatchVideoSnaphotTimes(driver).text
                        report["SnapshotTimes"]=tmp_sn_times
                        if sn_times:
                            if tmp_sn_times != sn_times:
                                sn_times = tmp_sn_times
                                s_time = time.time()
                            else:
                                continue
                        else:
                            break
                    report["LastSnapshotTime"] = datetime.fromtimestamp(s_time)
                else:
                    continue
        else:
            break
    return report
if __name__ == "__main__":
    pass
    