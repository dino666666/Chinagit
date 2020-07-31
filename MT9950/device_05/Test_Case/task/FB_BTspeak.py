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
log.open('FB_BTspeak')

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

    # 启动FileBlowser
    result, win = adb.app_start(times=3, keyword='filebrowser',
                                package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
    logO.info(win)

    # 判断FileBrowser是否启动成功
    if result == True:
        logO.info('FileBrowser started successfully')
    else:
        logO.info('FileBrowser startup failed')

    # 选择Video
    adb.left(3, 1)
    adb.ok(2, 2)

    # 播放60S
    for i in range(3):
        result,win = adb.windows('videoplayer.playcontrol')
        logO.info(win)

        if result == True:
            logO.info('视频正在播放...')
        else:
            logO.info('视频没有在播放...')

        time.sleep(20)

    adb.back(5)
    #启动Bluetooth Stereo
    result, win = adb.app_start(times=3, keyword='btspeaker',
                                package='com.oneplus.tv.btspeaker/.MainActivity')
    logO.info(win)

    # 判断Bluetooth Stereo是否启动成功
    if result == True:
        logO.info('Bluetooth Stereo started successfully')
    else:
        logO.info('Bluetooth Stereo startup failed')

    adb.ok(1,30)
    result,win = adb.windows('btspeaker')
    logO.info(win)

    if result == True:
        logO.info('音乐仍然在播放...')
    else:
        logO.info('音乐没有在播放...')


    adb.home()
    adb.down(6)
    adb.right(6)
    adb.up(5)
    adb.left(5)

    # 启动WiFi
    result, win = adb.app_start(times=3, keyword='NetworkActivity',
                                package='com.android.tv.settings/.connectivity.NetworkActivity')
    logO.info(win)

    if result == True:
        logO.info('WiFi started successfully')
    else:
        logO.info('WiFi startup failed')

    adb.ok(1,3)
    adb.left(3)
    adb.ok(1,5)

    # 启动FileBlowser
    result, win = adb.app_start(times=3, keyword='filebrowser',
                                package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
    logO.info(win)

    # 判断FileBrowser是否启动成功
    if result == True:
        logO.info('FileBrowser started successfully')
    else:
        logO.info('FileBrowser startup failed')

    adb.right(6)
    adb.ok(1,2)
    adb.down(5)
    adb.ok(1,5)

    for i in range(3):
        result,win = adb.windows('musicplayer')

        if result == True:
            logO.info('当前音频有在播放...')
        else:
            logO.info('当前音频没有在播放...')

        time.sleep(20)

    adb.back(5)

    logO.info('已执行完第' + str(num) + '次')