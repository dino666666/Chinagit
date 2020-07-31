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

# 创建一个队列
q=queue.Queue()

#实例化
#运行信息
logO = run_log(logging_path=runpath,logger=device).getlog()
#设备信息
adb = adb(device=device)
#logcat信息
log = log(log_path=logpath,device=device)

#脚本调试信息
logging.basicConfig(level=logging.DEBUG,format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

def thread():
    #判断是否需要退出脚本执行
    while True:
        end = input('请输入q结束程序:')
        if end == 'q':
            q.put('q')
            break

#script execution
logO.info('script execution')
time.sleep(2)

#初始化
initialize(device=device)
time.sleep(2)
adb.order('rm -rf /sdcard/*.png')

#初始化线程
thread_thred = threading.Thread(target=thread)
#打开线程
thread_thred.start()

#运行脚本前，清除历史logcat
adb.order('logcat -c')
logO.info('logcat -c')

time.sleep(2)
result,win = adb.app_start(times=25,keyword='btspeaker',
                           package='com.oneplus.tv.btspeaker/.MainActivity')
logO.info(win)

# 判断Bluetooth Stereo是否启动成功
if result == True:
    logO.info('Bluetooth Stereo started successfully')
else:
    logO.info('Bluetooth Stereo startup failed')

template_name = picturepath+'template.png'
# 截屏
adb.screencap(path=template_name)
time.sleep(2)
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

    # 打开logcat，模块命名为BTspeak
    log.open('BTspeak')
    result, win = adb.app_start(times=15, keyword='btspeaker',
                               package='com.oneplus.tv.btspeaker/.MainActivity')
    logO.info(win)

    # 判断Bluetooth Stereo是否启动成功
    if result == True:
        logO.info('Bluetooth Stereo started successfully')
    else:
        logO.info('Bluetooth Stereo startup failed')

    # 删除/sdcard下的所有.png文件
    adb.order('rm -rf /sdcard/*.png')
    # 获取当前时间并格式化
    pt = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    picture_name = picturepath+'BTspeak'+pt+'.png'
    #截图
    adb.screencap(path=picture_name)
    time.sleep(2)
    judge = os.path.exists(picture_name)

    # 检查PC本地是否存在需要对比的图像
    if judge == True:
        logO.info('开始进行图像比对...')

        # 开始进行图像比对，pass则将图片删除，fail则保留
        if compare(picture1=template_name,picture2=picture_name,value=0.99):
            logO.info('pass')
            time.sleep(1)
            os.remove(picture_name)#删除pass的图片
        else:
            logO.info('fail')
            logO.info('30S后再尝试一次...')
            time.sleep(30)
            # 删除/sdcard下的所有.png文件
            adb.order('rm -rf /sdcard/*.png')
            # 获取当前时间并格式化
            pt = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            picture_name = picturepath + 'BTspeak' + pt + '.png'
            # 截图
            adb.screencap(path=picture_name)
            time.sleep(2)
            judge = os.path.exists(picture_name)

            # 检查PC本地是否存在需要对比的图像
            if judge == True:
                logO.info('开始进行图像比对...')

                # 开始进行图像比对，pass则将图片删除，fail则保留
                if compare(picture1=template_name, picture2=picture_name,value=0.99):
                    logO.info('pass')
                    time.sleep(1)
                    os.remove(picture_name)  # 删除pass的图片
                    logO.info('已执行完第' + str(num) + '次')

            else:
                logO.info('30S Fail')
    else:
        time.sleep(2)
        initialize(device=device)
        time.sleep(10)

    logO.info('已执行完第' + str(num) + '次')
    time.sleep(3)