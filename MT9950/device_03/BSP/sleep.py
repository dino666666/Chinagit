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
# from lib.common.BasePage import Basepage
from lib.common.part_image import template_part
# 方法
# from lib.common.initialize import initialize
# from lib.common.template_matching import compare
from device_05.parameter import info

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

num = 0

log.open(module='STR')
while True:
    # 判断是否需要跳出循环，结束运行中的脚本
    if not q.empty():
        if q.get() == 'q':
            # 结束运行脚本时，关闭logcat的抓取
            log.close()
            logO.info('END')
            q.put('q')
            break

            # 每次循化num+temp
    num += 1
    # 写入运行信息
    logO.info('开始执行第' + str(num) + '次')

    adb.oneplus(type=1)
    result,window = adb.windows('ActionsDialog')
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
            result, coordinate = template_part(wifi_picture, name,num=0.64)

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
                    result, coordinate = template_part(wifi_picture, name,num=0.64)

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

    try:
        name = adb.screencap(path=picturepath, module='Sleep', type=1)
        judge = os.path.exists(name)
        # 检查PC本地是否存在需要对比的图像
        if judge == True:
            logO.info('====开始进行图像比对====')
            wifi_picture = picturepath + 'Setting.png'
            result, coordinate = template_part(wifi_picture, name,num=0.64)

            # 开始进行图像比对，pass则将图片删除，fail则保留
            if result == True:
                logO.info('Sleep logo pass')
                logO.info('Sleep up pass')
                time.sleep(1)
                # 删除pass的图片
                os.remove(name)
            else:
                logO.info('Sleep logo fail')
                logO.info('Sleep up fail')
                logO.info('再尝试检测一遍...')
                adb.home(2, 1)
                time.sleep(3)
                lt = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
                name = adb.screencap(path=picturepath, module='Sleep', type=1)
                judge = os.path.exists(name)

                if judge == True:  # 检查PC本地是否存在需要对比的图像
                    logO.info('====开始进行图像比对====')
                    result, coordinate = template_part(wifi_picture, name,num=0.64)

                    # 开始进行图像比对，pass则将图片删除，fail则保留
                    if result == True:
                        logO.info('Sleep logo pass')
                        logO.info('Sleep up pass')
                        time.sleep(1)
                        # 删除pass的图片
                        os.remove(name)
                    else:
                        logO.info('Sleep logo fail')
                        logO.info('Sleep up fail')
                        adb.order('input keyevent KEYCODE_POWER')
    except:
        adb.screencap(path=picturepath, type=1, module='Sleep_Error')

    time.sleep(5)

    logO.info('已执行第' + str(num) + '次')
