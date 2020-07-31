import datetime
import os
import time
import logging
import threading
import queue
import uiautomator2 as u2
import unittest
import ddt

# 类
from lib.common.adbevent import adb
from lib.common.runinfo import run_log
from lib.common.logcat import log
# from lib.common.BasePage import Basepage
# from lib.common.part_image import template_part
from device_04.parameter import info
from lib.common.read_txt import read_txt
from ddt import data,ddt


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@ddt
class Reboot(unittest.TestCase):
    def setUp(self) -> None:
        self.device, self.path = info()
        self.adb = adb(device=self.device)
        self.log = log(device=self.device, log_path=self.path)
        logpath = self.path + 'log/'
        picturepath = self.path + 'picture/'
        runpath = self.path + 'runinfo/'
        self.log0 = run_log(logging_path=runpath, logger=self.device).getlog()
        self.adb.order("monkey -p com.heytap.tv.launcher 1")
        self.log0.info("设备正在初始化")

    def tearDown(self) -> None:
        pass

    @data(*range(1,1000))
    def test_reboot(self,m):
        self.log0.info("每隔0.3S检测一次当前视窗，正在判断TV是否重启完成，请稍候....")
        while True:
            time.sleep(1)
            result, window = self.adb.windows('com.heytap.tv.launcher')
            if result == True:
                time.sleep(10)
                self.log0.info("TV已启动，准备进行下一次测试")
                self.adb.order("reboot")
                T0 = time.time()
                break
            else:
                # 获得当前时间
                now = datetime.datetime.now()
                # 转换为指定的格式:
                debug_time = now.strftime("%Y-%m-%d %H:%M:%S")
                logging.info("由于上一轮测试异常导致reboot命令无法输入，测试结束")
                logging.info("异常时间戳:" + str(debug_time))
                time.sleep(10)
                self.assertEqual(1, 2, '检测到TV重启异常')
        self.log0.info("第" + str(m) + "轮重启测试启动")
        while True:
            for i in range(45):
                time.sleep(1)
                global result1
                result1, window = self.adb.windows('com.heytap.tv.launcher')
                if result1:
                    time.sleep(1)
                    T1 = time.time()
                    T = T1 - T0
                    self.log0.info('重启耗时:' + str(T) + 'S')
                    time.sleep(5)
                    self.log0.info("重启后已进入桌面，本次重启正常")
                    self.assertEqual(1, 1, '重启正常')
                    time.sleep(10)
                    break
            if result1 ==False:

                # 获得当前时间
                now = datetime.datetime.now()
                # 转换为指定的格式:
                debug_time = now.strftime("%Y-%m-%d %H:%M:%S")
                logging.info("研发debug时间戳:" + str(debug_time))
                logging.info("未检测到TV进入桌面launcher，本次reboot失败")
                time.sleep(10)
                self.assertEqual(1, 2, '检测到TV reboot重启异常')
            break






