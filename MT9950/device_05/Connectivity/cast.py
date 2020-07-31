#_*_encoding:GBK*_

import time
import random
import logging
import threading
import queue

from lib.common.adbevent import adb
from lib.common.runinfo import run_log
from lib.common.logcat import log
from device_05.parameter import info

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
log.open('cast')

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
    applist = ['com.google.android.youtube.tv','com.graymatrix.did/com.zee5.splash.SplashActivity','com.netflix.ninja/.MainActivity',
               'com.amazon.amazonvideo.livingroom/com.amazon.ignition.IgnitionActivity','com.oneplus.tv.filebrowser/.ui.activity.MainActivity',
               'com.hungama.movies.tv/com.hungama.Activity.ActivityTermsOfUse']

    random_number = random.randint(0, 6)

    if random_number <= 5:
        adb.app_start(times=3, package=applist[random_number])
    else:
        adb.home()

    for i in range(30):
        time.sleep(3)
        result, win = adb.windows('apps.mediashell')
        logO.info(win)

        if result == True:
            break

    result,win = adb.windows('apps.mediashell')
    if result == True:
        logO.info('投屏成功')
        time.sleep(5)
        adb.back(1,60)
    else:
        logO.info('没有投屏')

    if random_number <=5:
        result,win = adb.windows(applist[random_number])
        logO.info(win)
        if result == True:
            logO.info('依然在原界面...')
        else:
            logO.info('已不在原界面...')