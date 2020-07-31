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
from lib.common.part_image import template_part
from lib.common.initialize import initialize
from device_05.parameter import info

#实例化一个队列，实现子线程与主进程之间的通讯
q = queue.Queue()
system_info = queue.Queue()

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
# 初始化
initialize(device=device)
adb.app_stop(times=3,package='com.google.android.youtube.tv')

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
    loginfo = adb.order('logcat')
    read = loginfo.readline()

    while read:

        if not q.empty():
            if q.get() == 'q':
                time.sleep(2)
                q.put('q')
                break

        if not system_info.empty():
            logO.info(system_info.get())
            logO.info(read)
            system_info.queue.clear()

        read = loginfo.readline()

def thread3():
    a = os.popen('adb -s ' + device + ' shell top -d 5')
    read = a.readline()
    number = 0

    while read:
        # print(read)
        if not q.empty():
            if q.get() == 'q':
                time.sleep(2)
                q.put('q')
                break

        info = read.split(' ')
        mem = 0
        mem_list = []
        for i in info:
            # print(i)
            if '%cpu' in i:
                total_cpu = i.split('%')[0]
                # print(i)
                # print(total_cpu)

            if 'idle' in i:
                # print(i)
                idle_cpu = i.split('%')[0]
                # print(idle_cpu)

                try:
                    use = int(total_cpu) - int(idle_cpu)
                    logO.info('当前CPU使用率:' + str(use) + '%')
                    if use > 390:
                        system_info.put('CPU')
                        print('cpu')
                        number += 1
                except:
                    pass

            if 'Mem' in i:
                # print(read)
                # print(info)
                mem = 1

            if mem == 1:
                if 'k' in i:
                    # print(i)
                    mem_list.append(i.split('k')[0])
                    # print(mem_list)
                    try:
                        buffers_mem = (int(mem_list[3]) / int(mem_list[0])) * 100
                        use_men = (int(mem_list[1]) / int(mem_list[0])) * 100
                        logO.info('当前内存使用率' + str(use_men) + "%")
                        logO.info('当前缓冲内存占据：' + str(buffers_mem) + '%')
                        if use_men > 99:
                            system_info.put('Mem')
                            print('mem')
                            number += 1

                        if use_men < 0.1:
                            system_info.put('buffers')
                            print('buff')
                            number += 1
                    except:
                        pass

        if number >= 1:
            logO.info(read)
            if number > 60:
                ps = adb.order('ps -ef').read()
                logO.info(ps)
                number = 0
            print('number:',number)
        read = a.readline()

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

# 打开logcat抓取log
log.open(module='SS_APP')

#定义一个数字，用作循环计数
num=0

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

    # 启动FileBlowser
    result, win = adb.app_start(times=3, keyword='filebrowser',
                                package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
    logO.info(win)

    # 判断FileBrowser是否启动成功
    if result == True:
        logO.info('FileBrowser started successfully')
    else:
        logO.info('FileBrowser startup failed')

    adb.left(3)
    adb.ok(2, 2)
    # 在FileBrowser播放60S
    time.sleep(50)
    random_number = random.randint(1,5)
    if random_number == 1:
    #启动ZEE5
        result,win=adb.app_start(times=25,keyword='zee5',package='com.graymatrix.did/com.zee5.splash.SplashActivity')

        logO.info(win)
        # 判断ZEE5是否启动成功
        if result == True:
            logO.info('ZEE5 started successfully')
        else:
            logO.info('ZEE5 startup failed')

        adb.down(2, 3)
        adb.ok(2, 3)
        time.sleep(60)
    elif random_number == 2:
        #启动Netflix
        result,win = adb.app_start(times=25,keyword='netflix',package='com.netflix.ninja/.MainActivity')

        logO.info(win)

        # 判断Netflix是否启动成功
        if result == True:
            logO.info('Netflix started successfully')
        else:
            logO.info('Netflix startup failed')

        adb.down(2,2)
        adb.ok(6,8)
        #播放60S
        time.sleep(60)
    elif random_number == 3:
        #启动Prime video
        result,win = adb.app_start(times=40,keyword='amazonvideo',package='com.amazon.amazonvideo.livingroom/com.amazon.ignition.IgnitionActivity')

        logO.info(win)
        # 判断Prime video是否启动成功
        if result == True:
            logO.info('Prime video started successfully')
        else:
            logO.info('Prime video  startup failed')
        #选择Prime video Home下的第一栏海报页的第一个视频播放
        adb.down(3, 1)
        adb.ok(1, 10)
        adb.down(2, 3)
        adb.ok(1, 10)
        adb.down(3)
        adb.left(3)
        #在Prime video 播放60S
        adb.ok(1, 60)
    elif random_number == 4:
        result,win = adb.app_start(times=20,keyword='youtube',package='com.google.android.youtube.tv')
        logO.info(win)

        # 判断YouTube是否启动成功
        if result == True:
            logO.info('YouTube started successfully')
        else:
            logO.info('YouTube  startup failed')
        #播放YouTube Home第一栏海报业的第一个视频
        adb.right(1, 3)
        #在YouTube播放60S
        adb.ok(1, 60)
        adb.home()
        time.sleep(3)
    else:
        result,win = adb.app_start(times=20,keyword='hungama.Activity.MainActivity',package='com.hungama.movies.tv/com.hungama.Activity.ActivityTermsOfUse')

        # 判断Hungama是否启动成功
        if result == True:
            logO.info('Hungama started successfully')
        else:
            logO.info('Hungama  startup failed')

        adb.right(1,2)
        adb.ok(1,20)
        result,win = adb.windows('PlayVideoActivity')

        if result == True:
            logO.info('Hungama正在播放')
        else:
            logO.info('Hungama可能没有在播放...')

        # 播放60S
        time.sleep(60)
        result, win = adb.windows('PlayVideoActivity')

        if result == True:
            logO.info('Hungama正在播放')
        else:
            logO.info('Hungama可能没有在播放...')

    adb.home()
    time.sleep(3)

    logO.info('已执行完第' + str(num) + '次')