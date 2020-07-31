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
w=queue.Queue()
#定义一个线程，用来判断是否仍处于FileBrowser界面，若不再则重新启动FileBrowser
def thread1():
    time.sleep(30)
    while True:

        if not w.empty():
            if w.get() == 'check_p':
                for i in range(5):
                    print(i)
                    time.sleep(2)
                adb.ok()
                w.queue.clear()

        result,window = adb.windows('videoplayer.playcontrol')

        if result == False:
            w.put('p')
            adb.home(1,1)
            adb.app_start(times=3,package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
            adb.left(3,1)
            adb.ok(2,2)
        time.sleep(2)
        logO.info(window)

        if not q.empty():
            if q.get() == 'q':
                logO.info('END')
                q.put('q')
                break

def thread2():
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

#初始化线程1
thread_thred1 = threading.Thread(target=thread1)
#打开线程
thread_thred1.start()
#初始化线程2
thread_thred2 = threading.Thread(target=thread2)
#打开线程2
thread_thred2.start()

#打开logcat，模块命名为PlaybackControl
log.open('PlaybackControl')

# 启动FileBlowser
result, win = adb.app_start(times=3, keyword='filebrowser',
                            package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
# 判断FileBrowser是否启动成功
if result == True:
    logO.info('FileBrowser started successfully')
else:
    logO.info('FileBrowser startup failed')

#选择Video
adb.left(3,1)
adb.ok(2,2)
#定义一个数字，用作循环计数
num=0

while True:
    #判断是否需要跳出循环，结束运行中的脚本
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
    #产生随机数，决定是播放视频或者是返回视频列表重新选择一个视频播放
    random_number = random.randint(1,12)
    event = random_number%3
    logO.info('event:'+str(event))

    if event != 0:
        number = 0

        for i in range(10):
            #产生随机数，决定快进、快腿、暂停、播放
            random_number = random.randint(1,12)
            event = random_number%4

            if random_number > 7:
                adb.right(event)
            else:
                adb.left(event)

            if random_number%4 == 0:
                adb.ok()
                number += 1
                print('number:',number)

            if not w.empty():
                if w.get() == 'p':
                    # 结束运行脚本时，关闭logcat的抓取
                    time.sleep(10)
                    w.queue.clear()
                    number=1
                    break
        #播控结束后，播放30S
        if number%2 == 1:
            adb.ok()
        else:
            pass
        time.sleep(30)
    else:
        w.put('check_p')
        adb.back()
        time.sleep(2)

        if event%5 == 1:
            adb.right(random_number)
            adb.ok()
        elif event%5 == 2:
            adb.down(random_number)
            adb.ok()
        elif event%5 == 3:
            adb.up(random_number)
            adb.ok()
        elif event%5 == 4:
            adb.left(random_number)
        else:
            adb.ok()

    #每执行10次随机事件，将返回视频列表随机选择视频播放
    if num%10 == 0:
        w.put('check_p')
        adb.back(1,2)
        if event % 5 == 1:
            adb.right(random_number)
            adb.ok()
        elif event % 5 == 2:
            adb.down(random_number)
            adb.ok()
        elif event % 5 == 3:
            adb.up(random_number)
            adb.ok()
        elif event % 5 == 4:
            adb.left(random_number)
        else:
            adb.ok()

    logO.info('已执行完第' + str(num) + '次')