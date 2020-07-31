#_*_encoding:GBK*_

import time
import random
import logging
import threading
import queue

from lib.common.adbevent import adb
from lib.common.runinfo import run_log
from lib.common.logcat import log
from device_02.parameter import info

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
    adb.ok()
    # 获取当前时间
    T0 = time.time()
    time.sleep(8)
    # 检查当前视窗
    result, win = adb.windows('com')
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

    T1 = time.time()

    if flag == 1:
        logO.info('重启成功')
    else:
        logO.info('重启失败')

    # 计算重启时间，大概
    T = T1 - T0
    logO.info('重启耗时:' + str(T) + 'S')

    time.sleep(10)
    # 判断重启后，是否处于Google Lanucher
    result, window = adb.windows('com.google.android.tvlauncher')
    logO.info(window)

    if result == True:
        logO.info('当前界面处于Google Lanucher')
    else:
        logO.info('当前界面不处于Google Lanucher')

    # 打开logcat，模块命名为FileBrowser
    log.open('FileBrowser')
    adb.netflix()
    time.sleep(30)
    result,win = adb.windows('netflix')
    logO.info(win)

    # 判断Netflix是否启动成功
    if result == True:
        logO.info('Netflix started successfully')
    else:
        logO.info('Netflix startup failed')

    adb.ok(1,30)
    adb.left(3,2)
    adb.up(1,3)
    adb.ok(1,10)
    adb.text('"you vs wild"')
    adb.right(3,2)
    adb.ok(2,5)
    time.sleep(60)