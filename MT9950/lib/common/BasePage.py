#_*_encoding:GBK*_
import os,time,threading
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Basepage(object):
    def __init__(self,device,driver,appPackage,appActivity,port,url):
        self.device=device
        self.driver = driver
        self.appPackage = appPackage
        self.appActivity = appActivity
        self.port=port
        self.url=url
    def Open(self):
    #打开测试APP，测试前的准备
        desired_caps={
            'platformName': 'android',
            'deviceName': 'device_test',
            'platformVersion': '9',
            'appPackage': 'appPackage',
            'appActivity': 'appActivity',
            # 'unicodeKeyboard':False,
            # 'resetKeyboard':False
            'MobileCapabilityType.CLEAR_SYSTEM_FILES':True,
            'newCommandTimeout':'3600',
            'udid':'device_test',
            'systemPort':'8200',
            # 'automationName':'UiAutomator2'
        }
        desired_caps['appPackage']=self.appPackage
        desired_caps['appActivity']=self.appActivity
        desired_caps['deviceName']=self.device
        desired_caps['udid']=self.device
        desired_caps['systemPort']=self.port
        self.driver = webdriver.Remote(self.url,desired_caps)
        # self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    def Quit(self):
        self.driver.quit()
        #测试完成需要还原环境

    def find_element(self,*loc):
        #超过20秒还没找到页面元素时则报异常，并截屏
        try:
            WebDriverWait(self.driver,20,1).until(EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except:
            lt = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            print(lt,'-找不到',*loc)
            time.sleep(1)

    def find(self,*loc):
        #尝试去寻找元素，找到则返回True
        try:
            WebDriverWait(self.driver,2,0.5).until(EC.visibility_of_element_located(loc))
            return True
        except:
            return False
