#_*_encoding:GBK*_
import time
import random
import logging
import threading
import queue

from lib.common.adbevent import adb
from lib.common.runinfo import run_log
from lib.common.logcat import log
from lib.common.initialize import initialize
from device_05.parameter import info
# 创建一个队列，实现子线程与主进程之间的通讯
q = queue.Queue()
w = queue.Queue()

#定义一个线程，用来判断是否仍处于FileBrowser界面，若不再则重新启动FileBrowser
def thread1():

    while True:
        if not w.empty():
            rights = int(w.get())
            print(rights)
            logO.info('进入异常处理流程...')
            initialize(device=device)
            # 启动FileBlowser
            result, win = adb.app_start(times=3, keyword='filebrowser',
                                        package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')

            # 判断FileBrowser是否启动成功
            if result == True:
                logO.info('FileBrowser started successfully')
            else:
                logO.info('FileBrowser startup failed')

            adb.right(rights,2)
            w.queue.clear()

        time.sleep(5)

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

#初始化
initialize(device=device)

#运行脚本前，清除历史logcat
adb.order('logcat -c')
logO.info('logcat -c')

#启动FileBlowser
result,win = adb.app_start(times=3,keyword='filebrowser',
                           package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
#判断FileBrowser是否启动成功
if result == True:
    logO.info('FileBrowser started successfully')
else:
    logO.info('FileBrowser startup failed')

# #初始化线程1
# thread_thred1 = threading.Thread(target=thread1)
# #打开线程
# thread_thred1.start()
#初始化线程2
thread_thred2 = threading.Thread(target=thread2)
#打开线程2
thread_thred2.start()

#打开logcat，模块命名为FileBrowser
log.open('FileBrowser_VIA')

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

    adb.ok(1,2)

    error = 0
    # 播放3个视频
    for i in range(3):
        adb.right(i,1)
        adb.ok(1,5)
        #获取当前视窗信息
        result,win = adb.windows('videoplayer.playcontrol')

        # 判断有没有进入播放界面
        if result == True:
            logO.info('视频正在播放...')
            time.sleep(60)
            result, win = adb.windows('videoplayer.playcontrol')

            if result == True:
                logO.info('视频正在播放...')
            else:
                logO.info('视频没有在播放...')
                error = 1
                break
        else:
            logO.info('视频没有在播放...')
            error = 1
            break

        adb.back(1,2)

    # 异常处理
    if error == 1:
        w.put('0')
        time.sleep(30)
        error = 0
    else:
        adb.back(1,2)

    # 播放10张图片
    adb.right(1,2)
    adb.ok(5,1)

    for i in range(10):
        # 判断有没有在播放图片
        result,win = adb.windows('gallery3d')
        logO.info(win)

        if result == True:
            logO.info('正在播放图片...')
        else:
            logO.info('图片没有在播放...')
            error = 1
            break

        adb.right(1,5)

    # 异常处理
    if error == 1:
        w.put('temp')
        time.sleep(30)
        error = 0
    else:
        adb.back(3, 2)

    # 播放3首音频
    adb.right(1,2)
    adb.ok(1,2)

    for i in range(3):
        adb.down(i,2)
        adb.ok(1,5)
        result,win = adb.windows('musicplayer')
        logO.info(win)

        if result ==True:
            logO.info('音频正在播放...')
        else:
            logO.info('音频没有在播放...')
            error = 1
            break

        time.sleep(30)

        result, win = adb.windows('musicplayer')
        logO.info(win)

        if result == True:
            logO.info('音频正在播放...')
        else:
            logO.info('音频没有在播放...')
            error = 1
            break

        adb.back(1,2)

    # 异常处理
    if error == 1:
        w.put('2')
        time.sleep(30)
        error = 0
    else:
        adb.back(1, 2)

    adb.left(5,1)

    logO.info('已执行完第'+str(num)+'次')