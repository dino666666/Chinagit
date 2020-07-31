#_*_encoding:GBK*_

import os
import time
import random
import logging
import threading
import queue

from lib.common.adbevent import adb
from lib.common.runinfo import run_log
from lib.common.logcat import log
from lib.common.bright import brightness
from lib.tools.camera_cap import picture
from device_03.parameter import info

#实例化一个队列，实现子线程与主进程之间的通讯
q=queue.Queue()

def thread():
    #判断是否需要退出脚本执行
    while True:
        end = input('请输入q结束程序:')
        if end == 'q':
            q.put('q')
            break

#初始化设备信息以及脚本运行过程中产生的文件保存路径
device,path = info()
#定义脚本运行过程中产生的文件路径
logpath = path + 'log/'
picturepath = path + 'picture/'
runpath = path + 'runinfo/'
#实例化
#运行信息
logO = run_log(logging_path=runpath,logger=device).getlog()
#设备信息
adb = adb(device=device)
#logcat信息
log = log(log_path=logpath,device=device)

#脚本调试信息
logging.basicConfig(level=logging.DEBUG,format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

#script execution
logO.info('script execution')
time.sleep(2)

#运行脚本前，清除历史logcat
adb.order('logcat -c')
logO.info('logcat -c')

#初始化线程
thread_thred = threading.Thread(target=thread)
#打开线程
thread_thred.start()

#定义一个数字，用作循环计数
num=0

while True:
    flag = 0
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
    adb.left(3, 1)
    command1 = 'adb -s ' + device + ' logcat -c'
    print(command1)
    os.system(command1)
    adb.ok()
    # 获取当前时间
    T0 = time.time()
    time.sleep(8)
    # 检查当前视窗
    result, win = adb.windows('mCurren')
    logO.info(result)
    logO.info(win)

    # 根据视窗信息，判断TV是否在重启，若否则用指令reboot重启
    if result == True:
        adb.order('reboot')
        T0 = time.time()

    # 每隔0.3S检测一次当前视窗，判断TV是否已经重启完成
    for i in range(180):
        time.sleep(0.3)
        result, window = adb.windows('com.google.android.tvlauncher')

        if result == True:
            flag = 1
            logO.info(window)
            time.sleep(3)
            break

    time.sleep(3)
    log.open(module='PQ')

    # 启动FileBlowser
    result, win = adb.app_start(times=3, keyword='filebrowser',
                                package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
    # 判断FileBrowser是否启动成功
    if result == True:
        logO.info('FileBrowser started successfully')
    else:
        logO.info('FileBrowser startup failed')
    # 选择Video
    adb.left(2)
    adb.right(2,1)
    adb.ok(1, 2)
    adb.right(2)
    adb.ok(1,5)
    time.sleep(5)

    picture_name = picture(path=picturepath,camera_number=0,mode='PQ')
    logO.info(picture_name)
    value = brightness(picture_name)

    print(value)
    logO.info('value:' + str(value))
    command = 'adb -s ' + device + ' shell getprop | grep -i picture'
    log_get = os.popen(command)
    log_read = log_get.read()
    logO.info(log_read)
    try:
        log_key = log_read.split(':')
        if 'Standard' in log_key[-1]:
            logO.info('PQ Pass')
            print('PASS')
        else:
            logO.info('PQ Fail')
            print('FAIL')
        print(log_key)
    except:
        logO.info('PQ Fail')
        print('FAIL')

    if int(value) >= 100:
        break

    logO.info('已执行第' + str(num) + '次')