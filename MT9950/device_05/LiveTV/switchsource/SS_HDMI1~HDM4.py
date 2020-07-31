#_*_encoding:GBK*_
#检测重启后蓝牙音箱的回链

import os
import time
import logging
import threading
import queue

# 类
from lib.common.adbevent import adb
from lib.common.runinfo import run_log
from lib.common.logcat import log
# 方法
from lib.common.initialize import initialize
from lib.common.template_matching import compare
from device_05.parameter import info

#初始化设备信息以及脚本运行过程中产生的文件保存路径
device,path = info()
#定义脚本运行过程中产生的文件路径
logpath = path + 'log/'
picturepath = path + 'picture/'
runpath = path + 'runinfo/'

# 创建队列
q=queue.Queue()
w=queue.Queue()
key=queue.Queue()
app=queue.Queue()

#实例化
#运行信息
logO = run_log(logging_path=runpath,logger=device).getlog()
#设备信息
adb = adb(device=device)
#logcat信息
log = log(log_path=logpath,device=device)

#脚本调试信息
logging.basicConfig(level=logging.DEBUG,format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

def thread1():
    #判断是否需要退出脚本执行
    while True:
        end = input('请输入q结束程序:')
        if end == 'q':
            q.put('q')
            break

        if not q.empty():
            if q.get() == 'q':
                q.put('q')
                time.sleep(2)
                logO.info('END')
                break

def thread2():
    text = adb.order('logcat -v time')
    read = text.readline()
    number = 0
    keyword = None
    flag = 0

    while read:
        if not q.empty():
            if q.get() == 'q':
                logO.info('END')
                q.put('q')
                break

        if not key.empty():
            keyword = key.get()
            logging.debug(keyword)
            flag = 1
            key.queue.clear()
            T0 = time.time()

        if flag == 1:
            number += 1
            if number % 100 == 0:
                T1 = time.time()
                T = T1 - T0

                if T >= 6:
                    w.put('none')
                    logging.debug('none')
                    logO.info(read)
                    flag = 0
                    number = 0

            if keyword in read:
                w.put('p')

        read = text.readline()

def thread3():
    while True:
        if not q.empty():
            if q.get() == 'q':
                q.put('q')
                time.sleep(2)
                logO.info('END')
                break

        time.sleep(2)
        if not app.empty():
            if app.get() == 'error':
                adb.back(5)
                time.sleep(1)
                adb.menu()
                time.sleep(3)
                adb.left(7)
                time.sleep(1)
                adb.ok(1,3)
                adb.left(9)
                key.put('HDMI1')
                adb.ok(1,3)
                logO.info('异常处理...')

                if w.get() == 'none':
                    logO.info('处理失败!')
                    logO.info('当前source不处于HDMI1')
                    adb.app_stop(times=3,package='com.oneplus.tv.android.livetv')
                    result, win = adb.app_start(times=3, keyword='livetv',
                                                package='com.oneplus.tv.android.livetv/.ActivityEntrance')
                    logO.info(win)

                    # 判断Live TV是否启动成功
                    if result == True:
                        logO.info('Live TV started successfully')
                    else:
                        logO.info('Live TV startup failed')

                    adb.down(3)
                    adb.ok(1,5)
                    adb.menu()
                    adb.left(5)
                    adb.ok(1,3)
                    adb.left(9)
                    key.put('HDMI1')
                    adb.ok(1,3)
                    logO.info('再次尝试异常处理...')

                    if w.get() == 'none':
                        logO.info('处理失败!')
                        logO.info('当前source不处于HDMI1')
                        logO.info('忽略异常，继续运行脚本...')
                    else:
                        pass
                else:
                    logO.info('处理成功')
                    logO.info('当前source处于HDMI1')

            app.queue.clear()

#script execution
logO.info('script execution')
time.sleep(2)

#初始化
initialize(device=device)
time.sleep(2)

#运行脚本前，清除历史logcat
adb.order('logcat -c')
logO.info('logcat -c')
time.sleep(2)
log.open('SS_HDMI')

#初始化线程1
thread_thred1 = threading.Thread(target=thread1)
#打开线程1
thread_thred1.start()
#初始化线程2
thread_thred2 = threading.Thread(target=thread2)
#打开线程2
thread_thred2.start()
#初始化线程3
thread_thred3 = threading.Thread(target=thread3)
#打开线程3
thread_thred3.start()

#传递关键字，用作判断是否处于HDMI1
key.put('HDMI1')
time.sleep(2)
result,win = adb.app_start(times=3,keyword='livetv',
                           package='com.oneplus.tv.android.livetv/.ActivityEntrance')
logO.info(win)

# 判断Live TV是否启动成功
if result == True:
    logO.info('Live TV started successfully')
else:
    logO.info('Live TV startup failed')

num=0

while True:

    if num == 0:
        if w.get() == 'none':
            logO.info('当前source不在HDMI1，不满足脚本执行条件...')
            logO.info('即将退出脚本运行...')
            q.put('q')
        else:
            logO.info('当前source 处于HDMI1,满足脚本执行条件')
            logO.info('脚本继续执行...')
            w.queue.clear()

    # 判断是否需要跳出循环，结束运行中的脚本
    if not q.empty():
        if q.get() == 'q':
            q.put('q')
            time.sleep(2)
            # 结束运行脚本时，关闭logcat的抓取
            log.close()
            logO.info('END')
            break

    # 每次循化num+temp
    num += 1
    # 写入运行信息
    logO.info('开始执行第' + str(num) + '次')

    # 切换到HDMI2
    adb.menu()
    time.sleep(3)
    adb.ok(1,2)
    adb.right(1,2)
    #根据log关键字HDMI2判断是否进入HDMI2
    key.put('HDMI2')
    adb.ok(1,2)

    if w.get() == 'none':
        logO.info('当前source不处于HDMI2')
    else:
        logO.info('当前source处于HDMI2')

    w.queue.clear()
    # 在HDMI2中播放10S
    time.sleep(10)
    # 切换到HDMI3
    adb.menu()
    time.sleep(3)
    adb.ok(1, 2)
    adb.right(1, 2)
    # 根据log关键字HDMI3判断是否进入HDMI3
    key.put('HDMI3')
    adb.ok(1, 2)

    if w.get() == 'none':
        logO.info('当前source不处于HDMI3')
    else:
        logO.info('当前source处于HDMI3')

    w.queue.clear()
    # 在HDMI3中播放10S
    time.sleep(10)
    # 切换到HDMI4
    adb.menu()
    time.sleep(3)
    adb.ok(1, 2)
    adb.right(1, 2)
    # 根据log关键字HDMI4判断是否进入HDMI4
    key.put('HDMI4')
    adb.ok(1, 2)

    if w.get() == 'none':
        logO.info('当前source不处于HDMI4')
    else:
        logO.info('当前source处于HDMI4')

    w.queue.clear()
    # 在HDMI4中播放10S
    time.sleep(10)
    # 切换到HDMI1
    adb.menu()
    time.sleep(3)
    adb.ok(1, 2)
    adb.left(6)
    # 根据log关键字HDMI2判断是否进入HDMI2
    key.put('HDMI1')
    adb.ok(1, 2)

    if w.get() == 'none':
        logO.info('当前source不处于HDMI1')
        #判断脚本执行异常，进入异常处理流程
        app.put('error')
        time.sleep(60)
    else:
        logO.info('当前source处于HDMI1')

    w.queue.clear()
    # 在HDMI2中播放10S
    time.sleep(10)
    logO.info('已执行完第' + str(num) + '次')
    time.sleep(3)
