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
from device_04.parameter import info

#实例化一个队列，实现子线程与主进程之间的通讯
q = queue.Queue()
w = queue.Queue()
key = queue.Queue()
system_info = queue.Queue()
thread_o = queue.Queue()

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

loginfo = adb.order('logcat')
def thread2():
    read = loginfo.readline()
    flag = 0
    keynum = 0

    while read:

        if not thread_o.empty():
            if thread_o.get() == 'q':
                thread_o.put('q')
                break

        if not q.empty():
            if q.get() == 'q':
                time.sleep(2)
                q.put('q')
                break

        if not system_info.empty():
            logO.info(system_info.get())
            logO.info(read)
            system_info.queue.clear()

        if not w.empty():
            result,win = adb.windows('filebrowser')
            if result == False:
                logO.info(read)
                logO.info('开始进行异常处理...')
                initialize(device=device)
                adb.app_stop(times=3, package='com.oneplus.tv.filebrowser')
                # 启动FileBrowser
                result, win = adb.app_start(times=3, keyword='filebrowser',
                                            package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
                # 判断FileBrowser是否启动成功
                if result == True:
                    logO.info('FileBrowser started successfully')
                else:
                    logO.info('FileBrowser startup failed')
                    logO.info('处理失败，忽略异常继续运行...')

                adb.left(3)
                adb.ok(2,3)
            w.queue.clear()
        if not key.empty():
            keyword = key.get()
            logO.info(keyword)
            flag = 1
            T0 = time.time()
            key.queue.clear()

        if flag == 1:
            keynum += 1

            if keyword in read and 'SettingsManagerService' in read:
                logO.info('模式切换成功')
                keynum = 0
                flag = 0

            if keynum >= 100:
                T1 = time.time()
                T = T1 - T0

                if T >= 10:
                    logO.info('模式切换失败...')
                    logO.info(read)
                    keynum = 0
                    flag = 0

        read = loginfo.readline()

a = os.popen('adb -s ' + device + ' shell top -d 5')
def thread3():
    read = a.readline()
    number = 0

    while read:
        # print(read)

        if not thread_o.empty():
            if thread_o.get() == 'q':
                thread_o.put('q')
                break

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

#打开logcat，模块命名为PlaybackControl
log.open('FB_SM')

# 启动FileBrowser
result, win = adb.app_start(times=3, keyword='filebrowser',
                            package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
# 判断FileBrowser是否启动成功
if result == True:
    logO.info('FileBrowser started successfully')
else:
    logO.info('FileBrowser startup failed')

#选择Video
adb.left(3)
adb.ok(2,2)
#定义一个数字，用作循环计数
num=0
modle = 0
# modle_list = ['Vivid','Custom','Cinema_Pro','Cinema_Home','Photo_Standard','Graphic','Standard']
modle_list = ['Dolby_Vision_Dark','Dolby_Vision_Bright']
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

    for m in modle_list:
        modle += 1
        print(m)

        for i in range(3):
            result,win = adb.windows('playcontrol')
            logO.info(win)

            if result == True:
                logO.info('视频正在播放')
            else:
                logO.info('视频可能没有在播放')
                w.put('p')

            time.sleep(20)

        logO.info('开始切换模式...')
        adb.menu(1,3)
        adb.down(3,2)
        adb.ok(1,3)
        adb.down(modle,2)
        key.put(m)
        adb.ok(1,3)

        for i in range(2):
            adb.back(1,1)
            result,win = adb.windows('videoplayer')
            logO.info(result)
            logO.info(win)

            if result == False:
                adb.ok(1,3)

        if modle >=1:
            modle = -1

    if num%50 == 0:
        thread_o.put('q')
        time.sleep(60)
        thread_o.queue.clear()
        time.sleep(5)
        # 初始化线程2
        thread_thred2 = threading.Thread(target=thread2)
        # 打开线程2
        thread_thred2.start()
        # 初始化线程3
        thread_thred3 = threading.Thread(target=thread3)
        # 打开线程3
        thread_thred3.start()

    logO.info('已执行完第' + str(num) + '次')