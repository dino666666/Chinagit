#_*_encoding:GBK*_

import time
import logging
import threading
import queue

from lib.common.adbevent import adb
from lib.common.runinfo import run_log
from lib.common.logcat import log
from lib.common.initialize import initialize
from device_05.parameter import info

#创建一个队列，实现子线程与主进程之间的通讯
q=queue.Queue()
w=queue.Queue()

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

#初始化
initialize(device=device)

#运行脚本前，清除历史logcat
adb.order('logcat -c')
logO.info('logcat -c')


def thread1():
    # 判断是否需要退出脚本执行
    while True:
        end = input('请输入q结束程序:')
        if end == 'q':
            q.put('q')
            break

def thread2():
    # 判断是否有退出FileBrowser
    while True:
        time.sleep(2)

        if not w.empty():

            if w.get() == 'p':
                # 关掉FileBrowser，并重新进入Video播放视频
                adb.app_stop(times=2,package='com.oneplus.tv.filebrowser')
                adb.app_start(times=3,keyword='filebrowser',
                              package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
                adb.left(3,1)
                adb.ok(2,2)

                w.queue.clear()

        if not q.empty():
            if q.get() == 'q':
                logO.info('END')
                q.put('q')
                break

#初始化线程1
thread_thred1 = threading.Thread(target=thread1)
#打开线程1
thread_thred1.start()
#初始化线程2
thread_thred2 = threading.Thread(target=thread2)
#打开线程2
thread_thred2.start()

#定义一个数字，用作循环计数
num=0

# 启动FileBlowser
result, win = adb.app_start(times=3, keyword='filebrowser',
                            package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
# 判断FileBrowser是否启动成功
if result == True:
    logO.info('FileBrowser started successfully')
else:
    logO.info('FileBrowser startup failed')
# 选择Video
adb.left(3, 1)
adb.ok(1, 2)

while True:
    flag=0
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
    adb.ok(1,2)
    time.sleep(3)
    result,win = adb.windows('playcontrol')
    logO.info(result)
    logO.info(win)

    if result == True:
        logO.info('正在播放视频。。')
    else:
        logO.info('视频没有在播放')
        adb.ok(1,3)
        result, win = adb.windows('playcontrol')
        logO.info(result)
        logO.info(win)

        if result == False:
            logO.info('视频没有在播放-尝试再次播放')
            w.put('p')
            time.sleep(30)

    adb.oneplus(type=1)

    for i in range(3):
        result,win=adb.windows('ActionsDialog')

        if result == True:
            pass
        else:
            adb.right(1,2)
            adb.oneplus(type=1)
            break
    adb.ok(1,15)
    adb.oneplus()

    logO.info('已执行完第' + str(num) + '次')
    time.sleep(3)
