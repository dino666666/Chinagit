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
from device_07.parameter import info

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
adb.order('logcat -c',type=1)
logO.info('logcat -c')

#初始化线程
thread_thred = threading.Thread(target=thread)
#打开线程
thread_thred.start()

#定义一个数字，用作循环计数
num=0

log.open('color')

while True:
    num += 1
    for i in range(6):
        for ti in range(3):
            adb.menu(num=1,times=5,type=1)
            result,window = adb.windows('com.android.tv.settings')
            if result == True:
                logO.info('Settings started successfully')
                break
            else:
                logO.info('Settings startup failed')
        adb.down(2,1)
        adb.ok(1,2)
        adb.down(2,1)
        adb.ok(1,2)
        adb.down(1,2)
        adb.ok(1,2)

        adb.down(i,1)
        adb.ok(1,2)
        for i in range(3):
            result, window = adb.windows('videoplayer')
            if result == True:
                break
            else:
                adb.back(1)

    result, window = adb.windows('videoplayer')
    if result == True:
        logO.info('videoplayer started successfully')
    else:
        logO.info('videoplayer startup failed')
        adb.ok(2)
    adb.ok()
    time.sleep(3)
    logO.info('已执行完第' + str(num) + '次')
