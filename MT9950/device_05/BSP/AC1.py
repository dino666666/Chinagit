import os
import time
import logging
import threading
import queue
import uiautomator2 as u2
import unittest
import ddt
import datetime

# 类
from lib.common.adbevent import adb
from lib.common.runinfo import run_log
from lib.common.logcat import log
# from lib.common.BasePage import Basepage
# from lib.common.part_image import template_part
from device_05.parameter import info
from lib.common.read_txt import read_txt
from ddt import data,ddt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@ddt
class Test_AC1(unittest.TestCase):
    def setUp(self) -> None:
        self.device, self.path = info()
        self.adb = adb(device=self.device)
        self.log = log(device=self.device, log_path=self.path)
        logpath = self.path + 'log/'
        picturepath = self.path + 'picture/'
        runpath = self.path + 'runinfo/'
        logO = run_log(logging_path=runpath, logger=self.device).getlog()
        logging.info("设备初始化完成")

    def tearDown(self) -> None:
        pass

    @data(*range(1,600))
    def test_AC1(self,m):
        logging.info("每隔0.3S检测一次当前视窗，判断TV是否已断电")
        while True:
        # 每隔0.3S检测一次当前视窗，判断TV是否已经重启完成
            time.sleep(0.3)
            # result, window = self.adb.windows('com.heytap.tv.oobe')
            result, window = self.adb.windows('com.heytap.tv.launcher')
            if result == False:
                flag = 1
                logging.info("检测到TV已断电")
                logging.info("第"+ str(m) + "次AC测试启动" )
                # logO.info(window)
                break

        logging.info("继电器断电30s")
        time.sleep(30)
        logging.info("继电器开始上电")
        time.sleep(15)
        logging.info("每隔1S检测一次当前视窗，判断TV是否进入桌面launcher")
        time.sleep(25)
        result, window = self.adb.windows('com.heytap.tv.launcher')
        if result == True:
            flag = 1
            # logO.info(window)
            time.sleep(1)
            self.adb.order("monkey -p com.heytap.tv.launcher 1")
            time.sleep(5)
            d = u2.connect_usb(self.device)
            # ele = d.xpath('//*[@text="精选"]')
            ele = d(text="精选")
            logging.info("TV已进入桌面launcher，本次测试正常")
            self.assertTrue(ele)
        else:
            logging.info("未检测到TV进入桌面launcher，本次开机失败")
            # 获得当前时间
            now = datetime.datetime.now()
            # 转换为指定的格式:
            debug_time = now.strftime("%Y-%m-%d %H:%M:%S")

            logging.info("研发debug时间戳:" + str(debug_time))
            time.sleep(110)
            self.assertEqual(1,2,'检测到TV重启异常')



