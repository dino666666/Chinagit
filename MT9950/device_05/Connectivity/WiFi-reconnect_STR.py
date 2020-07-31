#_*_encoding:GBK*_

import os
import time
import logging
import threading
import queue

# 类
from lib.common.adbevent import adb
from lib.common.runinfo import run_log
from lib.common.logcat import log
from lib.common.BasePage import Basepage
from lib.common.part_image import template_part
from appium.webdriver.common.mobileby import MobileBy
# 方法
from lib.common.initialize import initialize
from lib.common.template_matching import compare
from device_01.parameter import info

#初始化设备信息以及脚本运行过程中产生的文件保存路径
device,path = info()
#定义脚本运行过程中产生的文件路径
logpath = path + 'log/'
picturepath = path + 'picture/'
runpath = path + 'runinfo/'

# 创建队列
q=queue.Queue()

#实例化
#运行信息
logO = run_log(logging_path=runpath,logger=device).getlog()
#设备信息
adb = adb(device=device)
#logcat信息
log = log(log_path=logpath,device=device)
#WIFI
driver=Basepage(device=device,driver='driver',appPackage='com.android.tv.settings',
                appActivity='connectivity.NetworkActivity',port=8200,url='http://127.0.0.1:4723/wd/hub')

#脚本调试信息
logging.basicConfig(level=logging.DEBUG,format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

def thread():
    #判断是否需要退出脚本执行
    while True:
        end = input('请输入q结束程序:')
        if end == 'q':
            q.put('q')
            break

#初始化线程
thread_thred1 = threading.Thread(target=thread)
#打开线程
thread_thred1.start()

# 初始化
initialize(device=device)
#启动webdriver驱动
driver.Open()
#检查wifi开关是否为ON,为OFF时则打开
text = driver.find_element(MobileBy.XPATH,
                         '//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[temp]/android.widget.LinearLayout[2]/android.widget.Switch').text
if text == 'OFF':
    driver.find_element(MobileBy.XPATH,"//*[@text='Wi-Fi']").click()
else:
    pass

time.sleep(3)

num = 0

while True:
    #使用异常处理流程，防止找不到元素报错
    try:

        flag = 0
        # 判断是否需要跳出循环，结束运行中的脚本
        if not q.empty():
            if q.get() == 'q':
                # 结束运行脚本时，关闭logcat的抓取
                log.close()
                logO.info('END')
                q.put('q')
                break
        log.open('sleep')
        # 每次循化num+temp
        num += 1
        # 写入运行信息
        logO.info('开始执行第' + str(num) + '次')
        adb.oneplus(type=1)
        result, window = adb.windows('ActionsDialog')
        if result == True:
            adb.ok()
        else:
            adb.order('input keyevent KEYCODE_POWER')

        time.sleep(5)

        try:
            name = adb.screencap(path=picturepath, module='Sleep', type=1)
            judge = os.path.exists(name)
            # 检查PC本地是否存在需要对比的图像
            if judge == True:
                logO.info('====开始进行图像比对====')
                wifi_picture = picturepath + 'Setting.png'
                result, coordinate = template_part(wifi_picture, name, num=0.64)

                # 开始进行图像比对，pass则将图片删除，fail则保留
                if result == False:
                    logO.info('Setting logo fail')
                    logO.info(' Sleep pass')
                    time.sleep(1)
                    # 删除pass的图片
                    os.remove(name)
                else:
                    logO.info('Setting logo pass')
                    logO.info('Sleep fail')
                    logO.info('再尝试检测一遍...')
                    adb.home(2, 1)
                    time.sleep(3)
                    lt = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
                    name = adb.screencap(path=picturepath, module='Sleep', type=1)
                    judge = os.path.exists(name)

                    if judge == True:  # 检查PC本地是否存在需要对比的图像
                        logO.info('====开始进行图像比对====')
                        result, coordinate = template_part(wifi_picture, name, num=0.64)

                        # 开始进行图像比对，pass则将图片删除，fail则保留
                        if result == False:
                            logO.info('Setting logo fail')
                            logO.info('Sleep pass')
                            time.sleep(1)
                            # 删除pass的图片
                            os.remove(name)
                        else:
                            logO.info('Setting logo fail')
                            logO.info('Sleep fail')
                            adb.order('input keyevent KEYCODE_POWER')
        except:
            adb.screencap(path=picturepath, type=1, module='Sleep_Error')

        adb.oneplus()
        time.sleep(5)

        name = adb.screencap(path=picturepath, module='WiFi', type=1)
        judge = os.path.exists(name)
        # 检查PC本地是否存在需要对比的图像
        if judge == True:
            logO.info('====开始进行图像比对====')
            wifi_picture = picturepath + 'WiFi_ON.png'
            result, coordinate = template_part(wifi_picture, name)

            # 开始进行图像比对，pass则将图片删除，fail则保留
            if result == True:
                logO.info('WI-FI图标显示为connected...')
                logO.info('pass')
                logO.info('wake up success')
                time.sleep(1)
                # 删除pass的图片
                # os.remove(name)
            else:
                logO.info('WI-FI图标显示为disconnect...')
                logO.info('fail')
                logO.info('wake-up failure')
                logO.info('再尝试检测一遍...')
                adb.oneplus()
                time.sleep(3)
                adb.back(2)
                adb.home()
                time.sleep(5)
                lt = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
                name = adb.screencap(path=picturepath, module='WiFi', type=1)
                judge = os.path.exists(name)

                if judge == True:  # 检查PC本地是否存在需要对比的图像
                    logO.info('====开始进行图像比对====')
                    result, coordinate = template_part(wifi_picture, name)

                    # 开始进行图像比对，pass则将图片删除，fail则保留
                    if result == True:
                        logO.info('WI-FI图标显示为connected...')
                        logO.info('pass')
                        time.sleep(1)
                        # 删除pass的图片
                        os.remove(name)
                    else:
                        logO.info('WI-FI图标显示为disconnect...')
                        logO.info('wake-up failure')
                        adb.oneplus()
                        time.sleep(3)
                        adb.back(2)
                        adb.home()
                        logO.info('fail')
    except:
        logO.info('error')
        adb.screencap(path=picturepath, type=1, module='WiFi_Error')

    for i in range(3):

        result,window = adb.app_start(times=3,keyword='NetworkActivity',package='com.android.tv.settings/com.android.tv.settings.connectivity.NetworkActivity')
        if result == True:
            logO.info('WiFi started successfully')
            break
        else:
            logO.info('WiFi startup failed')
            adb.screencap(type=1,module='mode')

    wifi_flag = 0
    # 尝试3次去启动webdriver
    for i in range(5):
        try:
            driver.Open()
            time.sleep(5)
            #检查wifi回连状态
            if driver.find(MobileBy.XPATH,"//*[contains(@text,'Connect')]")==True:
                wifi_flag = 1
                driver.Quit()
                break
            else:
                wifi_flag = 0
                # 检查wifi开关是否为ON,为OFF时则打开
                text = driver.find_element(MobileBy.XPATH,
                                           '//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[temp]/android.widget.LinearLayout[2]/android.widget.Switch').text
                if text == 'OFF':
                    adb.screencap(path=picturepath, type=1, module='WiFi_Error')
                    logO.info('wifib switch is off')
                    driver.find_element(MobileBy.XPATH, "//*[@text='Wi-Fi']").click()
                else:
                    pass

                time.sleep(3)
                driver.Quit()
                break
        except:
            try:
                pass
            except:
                pass

    if wifi_flag == 0:
        logO.info('WI-FI回连失败...')
        adb.screencap(path=picturepath, type=1, module='WiFi_RC')
    else:
        logO.info('WI-FI回连成功...')

    adb.back(3,1)



    ping = adb.order('"ping -c 10 www.google.com"')
    read = ping.readline()

    while read:
        logO.info(read)
        drop = read.split(' ')

        for probability in drop:
            if '%' in probability:
                logO.info('丢包率:'+probability)

        read = ping.readline()
    log.close()
    logO.info('已执行第' + str(num) + '次')