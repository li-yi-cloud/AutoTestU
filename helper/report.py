'''
Created on 2018年7月26日

@author: cloud
'''
import logging
from threading import Lock
from pandas import DataFrame,ExcelWriter
import settings
from settings.template import server_url
import json,datetime,time
import copy

logger = logging.getLogger()

class ServerResponseDataMap():
    ''''''
    def __basetranslate(self,datamap,arg):
        if arg in datamap:
            return datamap[arg]
        else:
            return arg
        
    def matchStatus(self,arg):
        datamap = {
            1:"主动", #proactive
            2:"被动" #Passive
            }
        return self.__basetranslate(datamap, arg)
    
    def matchedUserGender(self,arg):
        datamap = {
            1:"male", # 男
            2:"female" # 女
            }
        return self.__basetranslate(datamap, arg)
    
    def matchedUserLevelName(self,arg):
        return arg
    
    def matchEroticismBehavior(self,arg):
        datamap = {
            True:"是",
            False:"否"
            }
        return self.__basetranslate(datamap, arg)
    
    def matchedUserChannel(self,arg):
        datamap = {
            0:"默认",
            1:"自然渠道",
            2:"install",
            3:"AEO or InApp"
            }
        return self.__basetranslate(datamap, arg)
    
    def circleGirl(self,arg):
        return self.matchEroticismBehavior(arg)
       
    def signGirl(self,arg):
        return self.matchEroticismBehavior(arg)
    
    def goddessGirl(self,arg):
        return self.matchEroticismBehavior(arg)
    
    def target(self,arg):
        datamap = {
            0:"其他",
            1:"女神",
            }
        return self.__basetranslate(datamap, arg)
    
    def matchMode(self,arg):
        datamap = {
            1:"global", # 全球
            2:"country" # 定向国家
            }
        return self.__basetranslate(datamap, arg)
    
    def createTime(self,arg):
#         logger.info("createTime  %s"%time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(arg/1000)))
        try:
#         return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(arg/1e3))
            return datetime.datetime.utcfromtimestamp(int(arg/1e3))
        except Exception as e:
            logger.warning("invalid time stamp,[%s]"%e)
            return arg

    def matchArea(self,arg):
        datamap = {
            0: 0,
            1: "泰国",
            2: "菲律宾",
            3: "印度尼西亚",
            4: "东南亚",
            5: "沙特阿拉伯",
            6: "阿拉伯联合酋长国",
            7: "科威特",
            8: "海湾国家",
            9: "埃及",
            10: "土耳其",
            11: "印度"
            }
        return self.__basetranslate(datamap, arg)
    
    def matchAreaName(self,arg):
        return arg
        
    def matchGender(self,arg):
#         logger.info("matchGender  %s"%self.matchedUserGender(arg))
        return self.matchedUserGender(arg)
    
    def matchUserPay(self,arg):
        datamap={
            0: "未付费",
            1: "付费"
            }
        return  self.__basetranslate(datamap, arg)

response_data_map = ServerResponseDataMap()

class PerfReport():
    def __init__(self):
        self.__columns = [
            "Account",
            "UserID",
            "Identity",
            "ClientMatchGender",
            "ClientMatchRegion",
            "RequestTimes",
            "MatchResult",
            "VideoResult",
            "MatchSpacingTime",
            "VideoSpacingTime",
            "ChannelID",
            "MatchedUserID",
            "MatchStatus",
            "MatchedUserGender",
            "MatchedUserLevelName",
            "MatchedEroticismBehavior",
            "MatchedUserChannel",
            "CircleGirl",
            "SignGirl",
            "GoddessGirl",
            "MatchMode",
            "CreateTime",
            "MatchAreaName",
            "Target",
            "MatchUserPay",
            "TrueUser"
            ]
        self.__df = DataFrame(columns=self.__columns)
        self.__lock = Lock()
        self.__httpclient = settings.http_client
        self.__resp_data_row_map = {
            "matchStatus": "MatchStatus",
            "matchedUserGender": "MatchedUserGender",
            "matchedUserLevelName": "MatchedUserLevelName",
            "matchEroticismBehavior": "MatchedEroticismBehavior",
            "matchedUserChannel": "MatchedUserChannel",
            "circleGirl": "CircleGirl",
            "signGirl": "SignGirl",
            "goddessGirl": "GoddessGirl",
            "matchMode": "MatchMode",
            "createTime": "CreateTime",
            "matchAreaName": "MatchAreaName",
            "target": "Target",
            "matchUserPay": "MatchUserPay"
            }
    
    '''
    append a row to DataFrame.
    support multi-threading
    '''
    def append(self,row,sleep_time=1.5):
        data = copy.deepcopy(row)
        time.sleep(sleep_time)
        self.get_remote(data)
        if self.__row_check(data):
            self.__lock.acquire()
            self.__df=self.__df.append(DataFrame(data,index=[0]), ignore_index=True,sort=False)
            self.__lock.release()
        else:
            logger.error("Invalid row : %s"%str(row))
        
    def get_remote(self,row):
        if row["MatchedUserID"] and ["UserID"]:
            try:
                logger.info("start request [%s]"%server_url.render(server=settings.server,UserID = row["UserID"],MatchedUserID = row["MatchedUserID"]))
                req = self.__httpclient.request("GET",server_url.render(server=settings.server, UserID = row["UserID"], MatchedUserID = row["MatchedUserID"]))
                remote_user_info = json.loads(req.data.decode("utf-8"))
                logger.info(remote_user_info)
                self.check_response(remote_user_info)
                for item in self.__resp_data_row_map:
#                     logger.info("get response key[%s]"%item)
                    if hasattr(response_data_map, item):
                        row[self.__resp_data_row_map[item]] = getattr(response_data_map, item)(remote_user_info[item])
                    else:
                        logger.warning("invalid column name %s")
            except Exception as e:
                logger.error("get remote user information error. reason: %s"%e)
    
    def check_response(self,data):
        for key in self.__resp_data_row_map:
            if key not in data:
                logger.warn("field '%s' is not in response data,will set to null."%key)
                data[key]=None
    
    def __row_check(self,row):
        if isinstance(row, dict):
            for key in row:
                if key in self.__columns:
                    pass
                else :
                    return False
        else:
            return False
        return True
    
    @property
    def to_dataframe(self):
        return self.__df
    
    @property
    def columns(self):
        return self.__columns
    
    def average(self,account,column):
        return self.__df.loc[self.__df["Account"]==account][column].mean()
    
    def count(self,account,column,condition):
        return self.__df.loc[self.__df["Account"]==account].loc[self.__df[column]==condition][column].count()
    
    def sum(self,account,column):
        return (self.__df.loc[self.__df["Account"]==account])[column].sum()
    
    def save_to_excel(self,file_name):
        report_writer = ExcelWriter(file_name)
        self.__df.loc[self.__df["MatchedUserID"]>500000000,["TrueUser"]] = "否"
        self.__df.loc[self.__df["MatchedUserID"]<500000000,["TrueUser"]] = "是"
        self.__df.to_excel(excel_writer=report_writer, sheet_name="Detail", encoding="gbk")
        #"MeanSpacingTime"
        average_spacing_df = self.__df.loc[:,["Account","UserID","Identity","ClientMatchGender","ClientMatchRegion"]].drop_duplicates()
        average_spacing_df["MeanMatchSpacingTime"] = None
        average_spacing_df["MeanVideoSpacingTime"] = None
        average_spacing_df["RequestTimesSum"] = None
        average_spacing_df["MatchedUser"] = None
        average_spacing_df["MatchedUserFalse"] = None
        average_spacing_df["MatchedUserTrue"] = None
        average_spacing_df["MatchedMale"] = None
        average_spacing_df["MatchedFemale"] = None
        average_spacing_df["PayUser"] = None
        
        accounts = self.__df["Account"].drop_duplicates()
        for account in accounts:
            average_spacing_df.loc[average_spacing_df["Account"] == account,["MeanMatchSpacingTime"]] = self.average(account,"MatchSpacingTime")
            average_spacing_df.loc[average_spacing_df["Account"] == account,["MeanVideoSpacingTime"]] = self.average(account,"VideoSpacingTime")     
            average_spacing_df.loc[average_spacing_df["Account"] == account,["RequestTimesSum"]] = self.sum(account,"RequestTimes")
            average_spacing_df.loc[average_spacing_df["Account"] == account,["MatchedUser"]] = (self.__df.loc[self.__df["Account"]==account])["Account"].count()
            average_spacing_df.loc[average_spacing_df["Account"] == account,["MatchedUserFalse"]] = (self.__df.loc[self.__df["Account"]==account])["MatchedUserID"].dropna(axis=0, how='any', inplace=False).loc[self.__df["MatchedUserID"]>500000000].count()
            average_spacing_df.loc[average_spacing_df["Account"] == account,["MatchedUserTrue"]] = (self.__df.loc[self.__df["Account"]==account])["MatchedUserID"].dropna(axis=0, how='any', inplace=False).loc[self.__df["MatchedUserID"]<500000000].count()     
            average_spacing_df.loc[average_spacing_df["Account"] == account,["MatchedMale"]] = (self.__df.loc[self.__df["Account"]==account])["MatchedUserGender"].dropna(axis=0, how='any', inplace=False).loc[self.__df["MatchedUserGender"]=="male"].count()
            average_spacing_df.loc[average_spacing_df["Account"] == account,["MatchedFemale"]] = (self.__df.loc[self.__df["Account"]==account])["MatchedUserGender"].dropna(axis=0, how='any', inplace=False).loc[self.__df["MatchedUserGender"]=="female"].count()
            average_spacing_df.loc[average_spacing_df["Account"] == account,["PayUser"]] = (self.__df.loc[self.__df["Account"]==account])["MatchUserPay"].dropna(axis=0, how='any', inplace=False).loc[self.__df["MatchUserPay"]=="付费"].count()
            
        average_spacing_df.reset_index(drop=True).to_excel(excel_writer=report_writer, sheet_name="statistics", encoding="gbk")        
        report_writer.save()
        
class PornographicClosureReport():
    ''''''
    def __init__(self):
        self.__columns = [
            "Account",
            "UserID",
            "Identity",
            "VideoStartTime",
            "FirstSnapshortTime",
            "LastSnapshotTime",
            "VideoTimes",
            "SnapshotTimes",
            "IsClosure",
            "ClosureTime",
            "IsUnlock",
            "CoinsBeforeUnlock",
            "CoinsAfterUnlock",
            "ClosureTimes",
            "UnlockPrice",
            "DeductionResult",
            "EroticismBehavior"
            ]
        self.__df = DataFrame(columns=self.__columns)
        self.__lock = Lock()
        self.__httpclient = settings.http_client
        self.__resp_data_row_map = {
#             "matchStatus": "MatchStatus",
#             "matchedUserGender": "MatchedUserGender",
#             "matchedUserLevelName": "MatchedUserLevelName",
            "matchEroticismBehavior": "MatchedEroticismBehavior",
#             "matchedUserChannel": "MatchedUserChannel",
#             "circleGirl": "CircleGirl",
#             "signGirl": "SignGirl",
#             "goddessGirl": "GoddessGirl",
#             "matchMode": "MatchMode",
#             "createTime": "CreateTime",
#             "matchAreaName": "MatchAreaName",
#             "target": "Target",
#             "matchUserPay": "MatchUserPay"
            }
    '''
    append a row to DataFrame.
    support multi-threading
    '''
    def append(self,row,sleep_time=1.5):
        data = copy.deepcopy(row)
        time.sleep(sleep_time)
        self.get_remote(data)
        data.pop("MatchedUserID")
        if self.__row_check(data):
            self.__lock.acquire()
            self.__df=self.__df.append(DataFrame(data,index=[0]), ignore_index=True,sort=False)
            self.__lock.release()
        else:
            logger.error("Invalid row : %s"%str(row))

    def get_remote(self,row):
        if row["MatchedUserID"] and ["UserID"]:
            try:
                logger.info("start request [%s]"%server_url.render(server=settings.server,UserID = row["MatchedUserID"],MatchedUserID = row["UserID"]))
                req = self.__httpclient.request("GET",server_url.render(server=settings.server, UserID = row["MatchedUserID"],MatchedUserID = row["UserID"]))
                remote_user_info = json.loads(req.data.decode("utf-8"))
                logger.info(remote_user_info)
                self.check_response(remote_user_info)
                row["EroticismBehavior"] = remote_user_info["matchEroticismBehavior"]
            except Exception as e:
                logger.error("get remote user information error. reason: %s"%e)
    
    def check_response(self,data):
        for key in self.__resp_data_row_map:
            if key not in data:
                logger.warn("field '%s' is not in response data,will set to null."%key)
                data[key]=None

    def __row_check(self,row):
        if isinstance(row, dict):
            for key in row:
                if key in self.__columns:
                    pass
                else :
                    return False
        else:
            return False
        return True
    
    def save_to_excel(self,filename):
        report_writer = ExcelWriter(filename)
        self.__df.to_excel(excel_writer=report_writer, sheet_name="sheet1", encoding="gbk")
        report_writer.save()
        
    @property
    def to_dataframe(self):
        return self.__df
if __name__=="__main__":
    pass