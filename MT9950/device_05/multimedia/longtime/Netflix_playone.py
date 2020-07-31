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

#实例化一个队列，实现子线程与主进程之间的通讯
q=queue.Queue()
thread_two = queue.Queue()

#运行脚本前，清除历史logcat
adb.order('logcat -c')
logO.info('logcat -c')

def thread1():
    #判断是否需要退出脚本执行
    while True:
        end = input('请输入q结束程序:')
        if end == 'q':
            q.put('q')
            break

def thread2():
    #判断是否需要退出脚本执行
    text = adb.order('logcat -v time')
    read = text.readline()
    number = 0
    flag = 0

    while read:
        if not q.empty():
            if q.get() == 'q':
                # 结束运行脚本时，关闭logcat的抓取
                log.close()
                logO.info('END')
                q.put('q')
                time.sleep(5)
                break

        if not thread_two.empty():
            if thread_two.get() == 'q':
                print('break')
                thread_two.queue.clear()
                time.sleep(2)
                break

        if 'state=2,' in read and flag == 0:
            print(read)
            time.sleep(10)
            adb.ok()
            flag = 1
            number = 0

        if flag == 1:
            number += 1

            if number >= 300:
                flag = 0

        read = text.readline()

#script execution
logO.info('script execution')
time.sleep(2)

#初始化线程1
thread_thred1 = threading.Thread(target=thread1)
#打开线程1
thread_thred1.start()
#初始化线程2
thread_thred2 = threading.Thread(target=thread2)
#打开线程2
thread_thred2.start()
#标志位,为1时结束循环
flag = 0
#开启抓取logcat
log.open('Netflix_playone')

while True:
    adb.up(3,1)
    adb.ok(5,5)

    for i in range(60):
        result,win = adb.windows('netflix')
        logO.info(win)

        if i % 10 ==0:
            adb.ok()

        if result == True:
            logO.info('当前界面处于Netflix')
        else:
            logO.info('当前界面不在Netflix中')
            logO.info('尝试重新启动Netflix。。。')
            time.sleep(3)
            # 启动Netflix
            result, win = adb.app_start(times=25, keyword='netflix', package='com.netflix.ninja/.MainActivity')
            logO.info(win)

            # 判断Netflix是否启动成功
            if result == True:
                logO.info('Netflix started successfully')
            else:
                logO.info('Netflix startup failed')

            adb.down(2, 2)
            adb.ok(6, 8)

        #判断是否需要跳出循环，结束运行中的脚本
        if not q.empty():
            if q.get() == 'q':
                # 结束运行脚本时，关闭logcat的抓取
                log.close()
                logO.info('END')
                q.put('q')
                flag=1
                time.sleep(5)
                break
        time.sleep(60)

    thread_two.put('q')
    time.sleep(5)
    # 初始化线程2
    thread_thred2 = threading.Thread(target=thread2)
    # 打开线程2
    thread_thred2.start()

    state = 3
    if flag == 1:
        break

