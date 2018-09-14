'''
Created on 2018年7月16日

@author: cloud
'''
import logging,time
from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy

logger = logging.getLogger()

class BaseElement():
    """
    The Base of appium element.
    This class must be used as a parent class to inherit.
    """
    def __init__(self,driver,verify_times=3,spacing_seconds=0.2):
        self.__driver = driver
        self.__element = None
        self.__verify_times = verify_times if isinstance(verify_times, int) and verify_times > 0 else 3
        self.__spacing_seconds = spacing_seconds if isinstance(spacing_seconds, (int,float)) and spacing_seconds > 0 and spacing_seconds < 10 else 1
    
    def set_config(self,verify_times=3,spacing_seconds=1):
        """set times about verify element and time spacing"""
        self.__verify_times = verify_times if isinstance(verify_times, int) and verify_times > 0 else 3
        self.__spacing_seconds = spacing_seconds if isinstance(spacing_seconds, (int,float)) and spacing_seconds > 0 and spacing_seconds < 10 else 1
        return self
    
    @property
    def selector(self):
        raise NotImplementedError("BaseElement.selector must be implemented in child class.")

    #verify a element 
    def __verify_element(self,by,value):
        logger.info(u'[%s]start find element: %s'%(self.__driver.session_id[-12:],self.ele_name))
        ret=False
        times = self.__verify_times
        for i in range(times):
            ret=self.__verify_element_(by, value,i==times-1)
            if ret:
                break
            else:
                time.sleep(self.__spacing_seconds)
        return ret
    
    def __verify_element_(self,by,value,islog=False):
        try:
            self.__element = self.__driver.find_element(by,value)
            return True
        except Exception as e:
            if islog:
                logger.warning(u'element is not found: %s reason:%s' %(self.ele_name,e))
            return False
        
    @property
    def element(self):
        if self:
            try:
                if not self.__element:
                    self.__element = self.__driver.find_element(*self.selector)
            except Exception as e:
                logger.warn("element error: %s"%e)
        return self.__element
    
    @property
    def text(self):
        str_text = ''
        if self.element:
            try:
                str_text = self.element.text
            except Exception as e:
                logger.warning("get %s text fail. reason: %s"%(self.ele_name,e))
        
        return str_text
        
    def __bool__(self):
        return True if self.__element else self.__verify_element(*self.selector) 
    
    def click(self):
        logger.info("start click %s."%str(self.ele_name))
        ret = False
        if self.element:
            try:
                self.element.click()
                ret = True
            except Exception as e:
                logger.error("click %s fail. reason: %s"%(self.ele_name,e))
        return ret
    
    @property
    def ele_name(self):
        return self.__class__.__name__
    
    @property
    def location(self):
        if self.element:
            return self.element.location
        else:
            return {"x":0,"y":0}
        
    @property
    def size(self):
        if self.element:
            return self.element.size
        else:
            return {"height":0,"width":0}
    
    def input_text(self,text):
        logger.info("start input [%s] to %s."%(text,self.ele_name))
        ret = False
        if self.element:
            try: 
                self.element.clear()
                self.element.send_keys(text)
                ret = True
            except Exception as e:
                logger.error("input [%s] to %s. reason: %s"%(text,self.ele_name,e))
        return ret
    
#skip ads in first page when open the application
class SkipFirstButton(BaseElement):
    '''click it when open application.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_skip")

#=================================================
#  common
#=================================================

class EnsureButton(BaseElement):
    '''common ensure button'''
    @property
    def selector(self):
        return (By.ID,"android:id/button1")

class CancelButton(BaseElement):
    '''common cancel button'''
    @property
    def selector(self):
        return (By.ID,"android:id/button2")
#==========================================
# Message page 
#==========================================
class MessageHomeButton(BaseElement):
    '''go to message page button.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/but_message")
    
class MessagePage(BaseElement):
    '''message page element ,used to verify current page is or not in message page.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/rv_chats")

class MessageLivUTeam(BaseElement):
    '''LivUTeam chat element.'''
    @property
    def selector(self):
        return (By.XPATH,"//amdroid.widget.TextView[@text='LivU Team']")

class MessageFriendsButton(BaseElement):
    '''click it to friends list'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/action_friend_list")

class MessageFriendsSearchImage(BaseElement):
    '''click it to open friend search page.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/iv_btn_end")

class MessageFriendsSearchInput(BaseElement):
    '''friend search input box element.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/et_input")

class MessageFriendsSearchButton(BaseElement):
    '''friend search confirm button.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/but_search_id")

class MessageFriendsSearchResult(BaseElement):
    '''friend search result element.'''
    @property
    def selector(self):
        return (By.XPATH,"//*[@resource-id='com.videochat.livu:id/fragment_search_result']/android.widget.LinearLayout")

class MessageFriendsAddByIDButton(BaseElement):
    '''The button of add a friend by user id.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/invites_view")

class MessageFriendsAddByIDInput(BaseElement):
    '''Input box when add a friend by user ID.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/ed_input")

class MessageFriendsAddByIDSearch(BaseElement):
    '''search friend by user ID button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/but_search")

class MessageFirendsAddByIDUserPraise(BaseElement):
    '''The user has number of raise'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/text_link")
    
class MessageFirendsAddByIDUserName(BaseElement):
    '''The user name.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/text_name")

class MessageFirendsAddByIDUserAddr(BaseElement):
    '''User location name'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/text_addres")

class MessageFirendsAddByIDAdd(BaseElement):
    '''add friend button,send a add friend message to people.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/text_send_msg")

class MessageFirendsAddByIDSendMSG(BaseElement):
    '''after add a friend,click it to chat with friend page'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/text_send_msg")
    
class MessageFriendsInviteByPhoneButton(BaseElement):
    '''invite a friend by phone button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/invites_view2")

class MessageFriendsChatPage(BaseElement):
    '''chat with friend page'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/_layout_bottom")

class MessageFriendsChatInput(BaseElement):
    '''text input box in chat with friend page'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/et_message")

class MessageFriendsChatSend(BaseElement):
    '''send text message to friend button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/ib_send")

class MessageFriendsChatGiftImage(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/container_gift_img")

class MessageFriendsChatGift(BaseElement):
    '''open gift list button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/ib_gift")

class MessageFriendsChatGifts(BaseElement):
    '''gift list'''
    @property
    def selector(self):
        return (By.XPATH,"//android.support.v4.view.ViewPager[@resource-id='com.videochat.livu:id/vp_gifts']")

class MessageFriendsChatImage(BaseElement):
    '''click it start to send a image to friend'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/ib_image")

class MessageFriendsChatEmojis(BaseElement):
    '''open emojis list button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/ib_emojis")

class MessageFriendsVideoChatButton(BaseElement):
    '''video chat button in chat with friend page'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/ib_video_chat")

class MessageFriendsVideoChatHangup(BaseElement):
    '''hang up button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/btn_hangup")

class MatchHomeButton(BaseElement):
    '''Match page button.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/but_home")

class MatchRequestElement(BaseElement):
    '''Match request times count element.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_request_count")

class MatchRemoteUserIdElement(BaseElement):
    '''Match video remote user id view element.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_remote_userid")
    
class MatchVideoChannelIdElement(BaseElement):
    '''Match channel id view element.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_channel_id")
    
class GenderFilterMatchButton(BaseElement):
    '''match a people with filter rule button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/but_gender")

class GenderFilterMatchButtonTv(BaseElement):
    '''match a people with filter rule button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_match_gender")
    
#匹配性别筛选界面
class GenderFilterMatchGoddessCheckBox(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/goddess_box")
    
class GenderFilterMatchAllCheckBox(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/gender_all_box")

class GenderFilterMatchMaleCheckBox(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/gender_male_box")

class GenderFilterMatchFemaleCheckBox(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/gender_female_box")

class RegionFilterMatchButton(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/but_region")

class RegionFilterMatchGlobal(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.XPATH,"//android.support.v7.widget.RecyclerView[@resource-id='com.videochat.livu:id/list_country']/android.view.View[1]")

class RegionFilterMatchOther(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.XPATH,"//android.support.v7.widget.RecyclerView[@resource-id='com.videochat.livu:id/list_country']/android.view.View[2]")

class GoddessWallEntranceElement(BaseElement):
    '''Entrance of goddess wall in match home.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/container_goddess_wall_entry")

class GoddessWallView(BaseElement):
    '''The view of goddess wall'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/pager_goddess")

class GoddessWallLanguages(BaseElement):
    '''Goddess wall language list.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/recycler_languages")

class GoddessWallEnglishLanguage(BaseElement):
    '''Goddess wall English language'''
    @property
    def selector(self):
        return (By.XPATH,"\\android.support.v7.widget.RecyclerView[@resource-id='com.videochat.livu:id/recycle_goddess']/android.widget.FrameLayout[1]/android.widget.TextView")

class GoddessWallFrenchLanguage(BaseElement):
    '''Goddess wall French language'''
    @property
    def selector(self):
        return (By.XPATH,"\\android.support.v7.widget.RecyclerView[@resource-id='com.videochat.livu:id/recycle_goddess']/android.widget.FrameLayout[2]/android.widget.TextView")

class GoddessWallIndonesianLanguage(BaseElement):
    '''Goddess wall Indonesian language'''
    @property
    def selector(self):
        return (By.XPATH,"\\android.support.v7.widget.RecyclerView[@resource-id='com.videochat.livu:id/recycle_goddess']/android.widget.FrameLayout[3]/android.widget.TextView")

class GoddessWallTurkishLanguage(BaseElement):
    '''Goddess wall Turkish language'''
    @property
    def selector(self):
        return (By.XPATH,"\\android.support.v7.widget.RecyclerView[@resource-id='com.videochat.livu:id/recycle_goddess']/android.widget.FrameLayout[4]/android.widget.TextView")

class GoddessCard(BaseElement):
    '''Goddess card in godess wall.'''
    @property
    def selector(self):
        return (By.XPATH,"android.support.v7.widget.RecyclerView[@resource-id='com.videochat.livu:id/recycle_goddess']/android.view.View[1]")

class GoddessName(BaseElement):
    '''Goddess name element in Goddess card.'''
    @property
    def selector(self):
        return (By.XPATH,"android.support.v7.widget.RecyclerView[@resource-id='com.videochat.livu:id/recycle_goddess']/android.view.View[1]/android.widget.TextView[@resource-id='com.videochat.livu:id/tv_name']")

class GoddessCountry(BaseElement):
    '''Goddess country element in Goddess card.'''
    @property
    def selector(self):
        return (By.XPATH,"android.support.v7.widget.RecyclerView[@resource-id='com.videochat.livu:id/recycle_goddess']/android.view.View[1]/android.widget.TextView[@resource-id='com.videochat.livu:id/tv_country']")

class GoddessVideoPrice(BaseElement):
    '''Goddess video price element in Goddess card.'''
    @property
    def selector(self):
        return (By.XPATH,"android.support.v7.widget.RecyclerView[@resource-id='com.videochat.livu:id/recycle_goddess']/android.view.View[1]/android.widget.TextView[3]")

class RechargeButton(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.XPATH,"//*[@resource-id='com.videochat.livu:id/ib_add_coin']/android.widget.TextView")
#         return (MobileBy.ANDROID_UIAUTOMATOR,"new UiSelector().text(\"Purchase\")")

class VideoingRemoveBlurButton(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/btn_hide')

class MatchVideoingFriendAddButton(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/img_firend_add')
    
class MatchStopEnsureButton(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/yes')

class MatchStopCancelButton(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/cancel')
    
class MatchConnectingNextButton(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/ib_next')

class MatchVideoingReportButton(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/ib_report')

class MatchVideoingFavoriteButton(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/img_favor')

class MatchingGenderFilterPopupConfirm(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/btn_confirm")

class MatchingGenderFilterPopupClose(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/ib_cancel")
    
class MatchingTips(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_connect_tip")

class MatchInfoElement(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_match_info")

class MatchVideoErrorInfoElement(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_match_info")

class MatchPornographicTestCheckBox(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/cb_porn_test")
    
class MatchPornographicPopUpElement(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_report_time_txt")

class MatchPornographicClosureTimeElement(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_clock_time")

class MatchLockReasonElement(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_cause_txt")

class MatchPornographicPopUpCancel(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/btn_negative")

class MatchPornographicPopUpUnlock(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/btn_positive")

class MatchPornographicPopUpTime(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_report_time_txt")

class MatchPornographicUnlockCoins(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_message")

class MatchPornographicIsSnapshot(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_snapshot")
    
class MatchPornographicAlert(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/but_allow")
    
class MatchPageCoinsElement(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/card_name")
    
class MatchVideoSnaphotTimes(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_snapshot_count")
    
class VideoingGiftButton(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/ib_gift')

class VideoingGifts(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/vp_gifts')

class VideoingTextChat(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/ib_video_chat')

class VideoingTextInput(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/et_message')

class VideoingSpeechButton(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/ib_speech')

class VideoingSpeechTips(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/speech_tips')

class VideoingStickerButton(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/ib_video_sticker')

class VideoingStickers(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/rv_stickers')
    
class VideoingObjectUserName(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/tv_title')

class VideoingObjectFavoriteNumber(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/tv_give')

class VideoingObjectLocation(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/tv_location')

class VideoingQuit(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/ib_video_quit')

class VideoingQuitText(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,'com.videochat.livu:id/text_quit')

# 匹配历史记录界面
class MatchHistoryButton(BaseElement):
    '''Match history button in Match page.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/img_history")
    
class MatchHistoryBackButton(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.XPATH,"//*[@resource-id='com.videochat.livu:id/toolbar']/android.widget.ImageButton")
#         return (MobileBy.ACCESSIBILITY_ID,"Navigate up")

class MatchHistoryStartMatchButton(BaseElement):
    '''Match history button in Match page.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/btn_start")

class MatchHistoryElement(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.XPATH,"//*[@resource-id='com.videochat.livu:id/toolbar']/android.widget.TextView")
#         return (MobileBy.ANDROID_UIAUTOMATOR,"new UiSelector().text(\"History\")")
    
class MatchHistoryCardSendMessaeButton(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.XPATH,"//*[@resource-id='com.videochat.livu:id/iv_chat']/android.widget.TextView")
#         return (MobileBy.ANDROID_UIAUTOMATOR,"new UiSelector().text(\"Send a message\")")

class MatchHistorySendMessageSpendCoinsTips(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"android:id/message")

class MatchHistoryCardReportButton(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/iv_report")

class MatchHistoryCardDeleteButton(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/iv_delete")

class MatchHistoryDeletePage(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"android:id/message")
    
class MatchHistoryReportTitle(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"android:id/alertTitle")
#         return (MobileBy.ANDROID_UIAUTOMATOR,"new UiSelector().text(\"Report user\")")

class MatchHistoryReportPornography(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.XPATH,"//*[resource-id=\"android:id/select_dialog_listview\"]/android.widget.TextView[1]")
#         return (MobileBy.ANDROID_UIAUTOMATOR,"new UiSelector().text(\"Pornographic behavior\")")

class MatchHistoryReportFakeGender(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.XPATH,"//*[resource-id=\"android:id/select_dialog_listview\"]/android.widget.TextView[2]")
#         return (MobileBy.ANDROID_UIAUTOMATOR,"new UiSelector().text(\"Fake gender\")")

class MatchHistoryReportLanguageViolence(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.XPATH,"//*[resource-id=\"android:id/select_dialog_listview\"]/android.widget.TextView[3]")
#         return (MobileBy.ANDROID_UIAUTOMATOR,"new UiSelector().text(\"Language violence\")")

class MatchHistoryReportOther(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.XPATH,"//*[resource-id=\"android:id/select_dialog_listview\"]/android.widget.TextView[4]")
#         return (MobileBy.ANDROID_UIAUTOMATOR,"new UiSelector().text(\"Others\")")


class MatchHistoryUserHeadImage(BaseElement):
    '''Match history user head image element.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/iv_headimg")

class MatchHistoryUserName(BaseElement):
    '''Match history user name element.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_name")

class MatchHistoryUserGenderAge(BaseElement):
    '''Match history user gender and age element.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_gender_age")

class MatchHistoryUserLocation(BaseElement):
    '''Match history user location element.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_locale")

class MatchHistoryMatchTime(BaseElement):
    '''Match history user match time element.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_time")

class MatchHistoryUserPraiseCount(BaseElement):
    '''Match history user praise count element.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/praise_count")
#============================================================
#user page
#============================================================
class UserHomeButton(BaseElement):
    '''User page button.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/but_personal")

class UserSetting(BaseElement):
    '''settings button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/iv_setting")
    
    
class UserSettingPageBody(BaseElement):
    '''settings page body'''
    @property
    def selector(self):
        return (By.XPATH,"//android.widget.LinearLayout[@resource-id='com.videochat.livu:id/item_version']/parent::android.widget.LinearLayout")
    
class UserSettingLogout(BaseElement):
    '''settings page logout button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_logout")

class UserSettingDeleteAccountButton(BaseElement):
    '''delete account button in setting page'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_delete_account")

class DeleteAccountReasonPage(BaseElement):
    '''delete account reason page'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/scrollview")

class DeleteAccountReasonHowToUse(BaseElement):
    '''delete account reason don't know how to use'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/radio_button1")

class DeleteAccountReasonMatchGirl(BaseElement):
    '''delete account reason can't match girl'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/radio_button2")

class DeleteAccountReasonBoring(BaseElement):
    '''delete account reason not found anyone interesting.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/radio_button3")

class DeleteAccountReasonPrivacy(BaseElement):
    '''delete account reason worry about privacy issues'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/radio_button4")

class DeleteAccountReasonNotifications(BaseElement):
    '''delete account reason too many notifications'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/radio_button5")

class DeleteAccountReasonOther(BaseElement):
    '''delete account reason other'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/radio_other")

class DeleteAccountReasonOtherInputBox(BaseElement):
    '''delete account reason other input box'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/et_bottom")

class DeleteAccountConfirm(BaseElement):
    '''confirm button about delete account'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_confirm")

class DeleteAccountUnderstandExplanationCheckbox(BaseElement):
    '''check box about read delete account explanation'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/cb_accept")

class UserSettingMessageNotificationSwitch(BaseElement):
    '''take on/off message notification'''
    @property
    def selector(self):
        return (By.XPATH,"//*[@resource-id='com.videochat.livu:id/item_switch_message']/android.widget.Switch")

class UserSettingBlurEffectSwitch(BaseElement):
    '''take on/off blur effect'''
    @property
    def selector(self):
        return (By.XPATH,"*[@resource-id='com.videochat.livu:id/item_switch_blur_notification']/android.widget.Switch")
 
class UserSettingBlackList(BaseElement):
    '''settings black list button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/item_blocklist")

class UserStore(BaseElement):
    '''go to coin store button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/item_store")

class UserInvite(BaseElement):
    '''invite friends button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/item_like_invite")

class UserGiftReceived(BaseElement):
    '''go to gift received page button.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/gift_layout")

class UserActivity(BaseElement):
    '''go to activity page button.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/item_activity")

class UserScanQR(BaseElement):
    '''go to Scan page button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/item_qr_scan")

class UserFAQ(BaseElement):
    '''go to FAQ page button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/item_feedback")

class UserFAQCheckElement(BaseElement):
    '''check FAQ page element.  Warning: only supported in android.'''
    @property
    def selector(self):
        return (MobileBy.ANDROID_UIAUTOMATOR,"new UiSelector().text(\"FAQ\")")

class UserShare(BaseElement):
    '''share application button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/item_share_facebook")

# ============================================================================
# sign in
class SignWithFacebook(BaseElement):
    '''button of sign with facebook accounts.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/ib_login_facebook")

class SignWithPhone(BaseElement):
    '''button of sign with phone number'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/login_btn_phone")

class SignWithPhoneCountryListview(BaseElement):
    '''country list in phone number'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/login_btn_phone")

class SignWithPhoneNumberInput(BaseElement):
    '''sign with phone number input'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/com_accountkit_phone_number")

class SignWithPhoneNext(BaseElement):
    '''next button of sign with phone number'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/com_accountkit_next_button")

class SignWithPhoneCodeInput_1(BaseElement):
    ''''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/com_accountkit_confirmation_code_1")

class SignWithPhoneCodeInput_2(BaseElement):
    ''''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/com_accountkit_confirmation_code_2")

class SignWithPhoneCodeInput_3(BaseElement):
    ''''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/com_accountkit_confirmation_code_3")

class SignWithPhoneCodeInput_4(BaseElement):
    ''''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/com_accountkit_confirmation_code_4")
    
class SignWithPhoneCodeInput_5(BaseElement):
    ''''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/com_accountkit_confirmation_code_5")

class SignWithPhoneCodeInput_6(BaseElement):
    ''''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/com_accountkit_confirmation_code_6")

class SigWithPhoneCodeNext(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/com_accountkit_next_button")
    
class SignWithPhoneFail(BaseElement):
    ''''''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/com_accountkit_start_over_button")
    
class MoreOptions(BaseElement):
    '''click it to sign/login with email page'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_account_more_option")

class MoreOpthonsBack(BaseElement):
    '''click it to sign with facebook/phone page'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_account_more_option")
        
class SignWithEmail(BaseElement):
    '''sign with email button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/btn_signup")

class SignEmailInput(BaseElement):
    '''input a email address in it,when sign with email'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/et_email") 

class SignPasswdInput(BaseElement):
    '''input a password in it,when sign with email'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/et_password") 
    
class SignWithEmailNextButton(BaseElement):
    '''next step button,when sign with email'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/btn_next") 

class LoginWithEmail(BaseElement):
    '''click it to login whit email address'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/btn_signin")
    
class LoginWithEmailConfirm(BaseElement):
    '''confirm button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/btn_signin")
        
class GenderFilterPopupMale(BaseElement):
    '''gender filter male check box'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/genderMaleView")

class GenderFilterPopupFemale(BaseElement):
    '''gender filter female check box'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/genderFeMaleView")

class GenderFilterPopupConfirm(BaseElement):
    '''continue button for gender filter popup'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/confirm")

class GenderFilterPopupClose(BaseElement):
    '''close button for gender filter popup.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/close")

class NewUserGiftPopupPurchase(BaseElement):
    '''Novice recharge popup'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_get_special_offer")

class NewUserGiftPopUpPurchaseSkip(BaseElement):
    '''in matching popup'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_skip")

class NewUserGiftPopupPurchaseClose(BaseElement):
    '''purchase popup close button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/iv_dialog_close")

class NewUserGiftPopupRatingBar(BaseElement):
    '''rating popup bar'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/ratingbar")

class NewUserGiftPopupRatingCancel(BaseElement):
    '''cancel button for rating.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/btn_cancel")

class NewUserGuideClose(BaseElement):
    '''close match rule tips'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/but_go_it")

class NewUserGuideMatchTips(BaseElement):
    '''click it to start match'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_tips_bot")

class PurchaseContinueButon(BaseElement):
    '''click it to purchase page.'''
    @property
    def selector(self):
        return (By.ID,"com.android.vending:id/continue_button")

class SignNameSettingInput(BaseElement):
    '''The input box of setting user name.'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/et_nickname")

class SignBirthdayInput(BaseElement):
    '''The input box of birthday setting'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/tv_birthday")

class SignBirthdayInputDone(BaseElement):
    '''click it to confirm a birthday'''
    @property
    def selector(self):
        return (By.ID,"android:id/button1")

class SignMaleCheckbox(BaseElement):
    '''click it to select male gender'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/view_male")

class SignFemaleCheckbox(BaseElement):
    '''click it to select female gender'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/view_female")

class SignConfirm(BaseElement):
    '''confirm button'''
    @property
    def selector(self):
        return (By.ID,"com.videochat.livu:id/btn_confirm")

#========================================================================================
# permission allow
#========================================================================================
class PermissionAllowButton(BaseElement):
    '''android permission allow button'''
    @property
    def selector(self):
        return (By.ID,"com.android.packageinstaller:id/permission_allow_button")

if __name__ == "__main__":
    pass