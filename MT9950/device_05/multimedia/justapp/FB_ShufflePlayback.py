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

#定义一个线程，用来判断是否仍处于FileBrowser界面，若不再则重新启动FileBrowser
def thread1():
    li = ['filebrowser','gallery3d','playcontrol','musicplayer','null']
    flag = 0

    while True:
        result,window = adb.windows(' ')
        for i in li:
            if i in window:
                flag = 1
                break

        if flag == 0:
            adb.app_start(package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
        time.sleep(2)
        logO.info(window)
        flag=0

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

#初始化线程1
thread_thred1 = threading.Thread(target=thread1)
#打开线程
thread_thred1.start()
#初始化线程2
thread_thred2 = threading.Thread(target=thread2)
#打开线程2
thread_thred2.start()

#打开logcat，模块命名为FileBrowser
log.open('FileBrowser')

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

    #无论进入Video或者是Audio都将循环3次
    for i in range(3):
        adb.left(4)
        # 产生随即数，随机进入Video、Image、Audio三个选项
        number = random.randint(0,2)
        adb.right(number)
        adb.ok(1,1)
        #获取当前视窗，用来判断进入Video或者是Audio
        result,window = adb.windows(' ')

        if 'com.oneplus.tv.filebrowser.ui.activity.ContentActivity' in window:
            #在Video循环3次
            for o in range(3):
                #产生随机数
                number = random.randint(1,8)
                #根据随机数产生随机事件，随机在列表选择其中一个播放（视频或者音乐）
                event = number%4
                if number > 4:
                    adb.right(event)
                else:
                    adb.down(event)
                adb.ok(1,1)
                result, window = adb.windows(' ')

                #判断播放的是视频还是音频
                if 'videoplayer.playcontrol' in window:
                    logO.info('进入视频播放。。')
                    logging.debug('videoplayer.playcontrol')
                    #判断播放的是视频时，执行随机播控事件
                    number = random.randint(0,8)
                    event = number%4
                    if number > 4:
                        adb.right(event)
                    else:
                        adb.left(event)
                    adb.ok(event,number)
                elif 'com.oneplus.tv.musicplayer.activity.MainActivity' in window:
                    logO.info('进入音频播放。。')
                    #判断播放的是音频时，执行随机播控事件
                    number = random.randint(0,8)
                    event = number%3

                    if event == 1:
                        logging.debug('music1')
                        adb.left(1,1)
                        adb.ok(1,3)
                        adb.right()
                    elif event == 2:
                        logging.debug('music2')
                        adb.right(1,1)
                        adb.ok(1,3)
                        adb.left()
                    else:
                        logging.debug('music else')
                        adb.up(2,1)

                        if number > 4:
                            for i in range(event):
                                adb.left(type=1)
                        else:
                            for i in range(event):
                                adb.right(type=1)
                        adb.down(1,10)

                else:
                    break
        #判断当前是否处于Image
        elif 'com.android.gallery3d.app.Gallery' in window:
            logO.info('播放图片。。')
            #产生随机数，进行左滑或者又滑
            number = random.randint(0,4)
            adb.right(number)
            adb.ok(1,1)
            number = random.randint(0, 6)
            adb.right()
            adb.ok(1,1)
            number = random.randint(0, 1)

            for i in range(0,3):

                if number == 1:
                    adb.left(type=1)
                else:
                    adb.right(type=1)
                time.sleep(3)

            adb.ok(2)
        else:
            pass

        logging.debug('开始返回..')
        adb.back(2,1)

        #返回到Video、Audio、Image选项
        for i in range(3):
            result,window=adb.windows('com.oneplus.tv.filebrowser.ui.activity.MainActivity')

            if result == True:
                break
            else:
                adb.back(1,1)
