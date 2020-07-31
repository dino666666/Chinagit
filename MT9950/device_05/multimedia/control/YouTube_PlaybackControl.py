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
w = queue.Queue()
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

        if not w.empty():
            result,win = adb.windows('youtube')
            if result == False:
                logO.info(read)
                logO.info('开始进行异常处理...')
                initialize(device=device)
                adb.app_stop(times=3, package='com.google.android.youtube.tv')
                # 启动YouTube
                result, win = adb.app_start(times=35, keyword='youtube',
                                            package='com.google.android.youtube.tv')
                # 判断YouTube是否启动成功
                if result == True:
                    logO.info('YouTube started successfully')
                else:
                    logO.info('YouTube startup failed')
                    logO.info('处理失败，忽略异常继续运行...')

                adb.ok(1,5)
            w.queue.clear()
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
log.open('PlaybackControl')

# 启动YouTube
result, win = adb.app_start(times=35, keyword='youtube',
                            package='com.google.android.youtube.tv')
# 判断YouTube是否启动成功
if result == True:
    logO.info('YouTube started successfully')
else:
    logO.info('YouTube startup failed')

#选择Video
adb.ok(1,40)
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
    adb.up(2,2)

    # 截图，获取进度条坐标,检查正常播放
    for i in range(3):
        template_name = picturepath + 'YouTube_bar.png'
        picture_name = adb.screencap(path=picturepath, module='YouTube', type=1)
        judge = os.path.exists(picture_name)

        # 判断截图是否存在
        if judge == True:
            try:
                result = False
                result,coordinate_value1 = template_part(picture1=template_name,picture2=picture_name,type = 1)
                logO.info('coordinate_value1[0]：' + str(coordinate_value1[0]))
                logO.info('coordinate_value1[temp]：' + str(coordinate_value1[1]))
            except:
                w.put('p')
                time.sleep(60)
            finally:
                #找到进度条，判断有进入视频播放
                if result == True:
                    logO.info('存在进度条...')
                else:
                    logO.info('找不到进度条...')


            template_name = picturepath + 'YouTube_play.png'
            try:
                result = False
                result, coordinate_value = template_part(picture1=template_name, picture2=picture_name)
            except:
                w.put('p')
                time.sleep(60)
            finally:
                 # 判断视频是在播放还是在暂停
                if result == True:
                    logO.info('当前播放状态为：Play')
                else:
                    logO.info('当前播放可能处于暂停')
                    adb.ok(1,2)

                time.sleep(60)
            # 计算进度条坐标差值
            adb.up(2,2)
            template_name = picturepath + 'YouTube_bar.png'
            picture_name = adb.screencap(path=picturepath, module='YouTube', type=1)
            judge = os.path.exists(picture_name)

            # 判断截图是否存在
            if judge == True:
                try:
                    result = False
                    difference_value = 0
                    result, coordinate_value2 = template_part(picture1=template_name, picture2=picture_name, type=1)
                    logO.info('coordinate_value2[0]：' + str(coordinate_value2[0]))
                    logO.info('coordinate_value2[temp]：' + str(coordinate_value2[1]))
                    difference_value = int(coordinate_value2[0]) - int(coordinate_value1[0])
                except:
                    w.put('p')
                finally:
                    # 找到进度条，判断有进入视频播放
                    if result == True:
                        logO.info('存在进度条...')
                    else:
                        logO.info('找不到进度条...')

                    logO.info('difference_value（播放）:' + str(difference_value))

                    if difference_value > 10:
                        logO.info('进度条有在走动,视频正在播放...')
                    else:
                        logO.info('进度条没有在走动,视频可能没在播放')
                        w.put('p')
                        time.sleep(60)

            print('break')
            break

        else:
            w.put('p')
            time.sleep(60)

    adb.ok(2,2)

    # 截图，获取进度条坐标,检查播控
    for i in range(3):
        template_name = picturepath + 'YouTube_pause.png'
        picture_name = adb.screencap(path=picturepath, module='YouTube', type=1)
        judge = os.path.exists(picture_name)

        # 判断截图是否存在
        if judge == True:
            try:
                result = False
                result, coordinate_value1 = template_part(picture1=template_name, picture2=picture_name)
            except:
                w.put('p')
                time.sleep(60)
            finally:
                # 根据图标判断视频是否在暂停
                if result == True:
                    logO.info('视频已暂停...')
                else:
                    logO.info('视频未暂停...')

            adb.up(1,2)
            template_name = picturepath + 'YouTube_bar.png'
            picture_name = adb.screencap(path=picturepath, module='YouTube', type=1)
            judge = os.path.exists(picture_name)

            # 判断截图是否存在
            if judge == True:
                try:
                    result, coordinate_value1 = template_part(picture1=template_name, picture2=picture_name)
                    logO.info('coordinate_value1[0]：' + str(coordinate_value1[0]))
                    logO.info('coordinate_value1[temp]：' + str(coordinate_value1[1]))
                except:
                    w.put('p')
                    time.sleep(60)
                finally:
                    if result == True:
                        logO.info('存在进度条...')
                    else:
                        logO.info('找不到进度条...')

            adb.left(8,1,type=1)

            template_name = picturepath + 'YouTube_bar.png'
            picture_name = adb.screencap(path=picturepath, module='YouTube', type=1)
            judge = os.path.exists(picture_name)

            # 判断截图是否存在
            if judge == True:
                try:
                    result = False
                    result, coordinate_value = template_part(picture1=template_name, picture2=picture_name)
                    logO.info('coordinate_value[0]：' + str(coordinate_value[0]))
                    logO.info('coordinate_value[temp]：' + str(coordinate_value[1]))
                except:
                    w.put('p')
                    time.sleep(60)
                finally:
                    if result == True:
                        logO.info('进度条移动成功...')
                    else:
                        logO.info('进度条移动失败...')

            # 播放视频
            adb.ok(1,10)
            adb.up(2,2)
            template_name = picturepath + 'YouTube_bar.png'
            picture_name = adb.screencap(path=picturepath, module='YouTube', type=1)
            judge = os.path.exists(picture_name)

            # 判断截图是否存在
            if judge == True:
                try:
                    result = False
                    difference_value = 0
                    result, coordinate_value2 = template_part(picture1=template_name, picture2=picture_name)
                    logO.info('coordinate_value[0]：' + str(coordinate_value2[0]))
                    logO.info('coordinate_value[temp]：' + str(coordinate_value2[1]))
                    difference_value = int(coordinate_value2[0]) - int(coordinate_value1[0])
                except:
                    w.put('p')
                    time.sleep(60)
                finally:
                    if result == True:
                        logO.info('存在进度条...')
                    else:
                        logO.info('找不到进度条...')


            logO.info('difference_value（快退）:' + str(difference_value))

            if difference_value < -10:
                logO.info('快退成功...')
            else:
                logO.info('快退失败...')
                w.put('p')
                time.sleep(60)

            adb.up(2, 2)
            adb.right(3,1,type=1)
            template_name = picturepath + 'YouTube_bar.png'
            picture_name = adb.screencap(path=picturepath, module='YouTube', type=1)
            judge = os.path.exists(picture_name)

            if judge == True:
                try:
                    result, coordinate_value = template_part(picture1=template_name, picture2=picture_name, type=1)
                    logO.info('coordinate_value[0]：' + str(coordinate_value[0]))
                    logO.info('coordinate_value[temp]：' + str(coordinate_value[1]))
                except:
                    w.put('p')
                    time.sleep(60)
                finally:
                    # 找到进度条，判断有进入视频播放
                    if result == True:
                        logO.info('存在进度条...')
                    else:
                        logO.info('找不到进度条...')

            adb.ok(1,3)
            adb.up(2,2)
            template_name = picturepath + 'YouTube_bar.png'
            picture_name = adb.screencap(path=picturepath, module='YouTube', type=1)
            judge = os.path.exists(picture_name)

            if judge == True:
                try:
                    result = False
                    difference_value = 0
                    result, coordinate_value3 = template_part(picture1=template_name, picture2=picture_name, type=1)
                    logO.info('coordinate_value3[0]：' + str(coordinate_value3[0]))
                    logO.info('coordinate_value3[temp]：' + str(coordinate_value3[1]))
                    difference_value = int(coordinate_value3[0]) - int(coordinate_value2[0])
                except:
                    w.put('p')
                    time.sleep(60)
                finally:
                    # 找到进度条，判断有进入视频播放
                    if result == True:
                        logO.info('存在进度条...')
                    else:
                        logO.info('找不到进度条...')

                logO.info('difference_value（快进）:' + str(difference_value))

                if difference_value > 10:
                    logO.info('快进成功...')
                else:
                    logO.info('快进失败...')

            print('break')
            break

        else:
            w.put('p')
            time.sleep(60)

    if num %3 == 0:
        adb.down(2,2)
    else:
        pass

    adb.ok(1,25)

    time.sleep(10)
    logO.info('break')

    logO.info('已执行完第'+str(num)+'次')