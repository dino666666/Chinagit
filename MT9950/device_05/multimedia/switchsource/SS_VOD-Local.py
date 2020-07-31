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

#ʵ����һ�����У�ʵ�����߳���������֮���ͨѶ
q = queue.Queue()
system_info = queue.Queue()

#��ʼ���豸��Ϣ�Լ��ű����й����в������ļ�����·��
device,path = info()
#����ű����й����в������ļ�·��
logpath = path + 'log/'
picturepath = path + 'picture/'
runpath = path + 'runinfo/'
#ʵ����
#������Ϣ
logO = run_log(logging_path=runpath,logger=device).getlog()
#�豸��Ϣ
adb = adb(device=device)
#logcat��Ϣ
log = log(log_path=logpath,device=device)

#�ű�������Ϣ
logging.basicConfig(level=logging.DEBUG,format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

#script execution
logO.info('script execution')
time.sleep(2)
# ��ʼ��
initialize(device=device)
adb.app_stop(times=3,package='com.google.android.youtube.tv')

#���нű�ǰ�������ʷlogcat
adb.order('logcat -c')
logO.info('logcat -c')

def thread1():
    #�ж��Ƿ���Ҫ�˳��ű�ִ��
    while True:
        end = input('������q��������:')
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
                    logO.info('��ǰCPUʹ����:' + str(use) + '%')
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
                        logO.info('��ǰ�ڴ�ʹ����' + str(use_men) + "%")
                        logO.info('��ǰ�����ڴ�ռ�ݣ�' + str(buffers_mem) + '%')
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

#��ʼ���߳�1
thread_thred1 = threading.Thread(target=thread1)
#���߳�1
thread_thred1.start()
#��ʼ���߳�2
thread_thred2 = threading.Thread(target=thread2)
#���߳�2
thread_thred2.start()
#��ʼ���߳�3
thread_thred3 = threading.Thread(target=thread3)
#���߳�3
thread_thred3.start()

# ��logcatץȡlog
log.open(module='SS_APP')

#����һ�����֣�����ѭ������
num=0

while True:
    flag=0
    #�ж��Ƿ���Ҫ����ѭ�������������еĽű�
    if not q.empty():
        if q.get() == 'q':
            # �������нű�ʱ���ر�logcat��ץȡ
            log.close()
            logO.info('END')
            q.put('q')
            break

    # ÿ��ѭ��num+temp
    num += 1
    # д��������Ϣ
    logO.info('��ʼִ�е�' + str(num) + '��')

    # ����FileBlowser
    result, win = adb.app_start(times=3, keyword='filebrowser',
                                package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
    logO.info(win)

    # �ж�FileBrowser�Ƿ������ɹ�
    if result == True:
        logO.info('FileBrowser started successfully')
    else:
        logO.info('FileBrowser startup failed')

    adb.left(3)
    adb.ok(2, 2)
    # ��FileBrowser����60S
    time.sleep(50)
    random_number = random.randint(1,5)
    if random_number == 1:
    #����ZEE5
        result,win=adb.app_start(times=25,keyword='zee5',package='com.graymatrix.did/com.zee5.splash.SplashActivity')

        logO.info(win)
        # �ж�ZEE5�Ƿ������ɹ�
        if result == True:
            logO.info('ZEE5 started successfully')
        else:
            logO.info('ZEE5 startup failed')

        adb.down(2, 3)
        adb.ok(2, 3)
        time.sleep(60)
    elif random_number == 2:
        #����Netflix
        result,win = adb.app_start(times=25,keyword='netflix',package='com.netflix.ninja/.MainActivity')

        logO.info(win)

        # �ж�Netflix�Ƿ������ɹ�
        if result == True:
            logO.info('Netflix started successfully')
        else:
            logO.info('Netflix startup failed')

        adb.down(2,2)
        adb.ok(6,8)
        #����60S
        time.sleep(60)
    elif random_number == 3:
        #����Prime video
        result,win = adb.app_start(times=40,keyword='amazonvideo',package='com.amazon.amazonvideo.livingroom/com.amazon.ignition.IgnitionActivity')

        logO.info(win)
        # �ж�Prime video�Ƿ������ɹ�
        if result == True:
            logO.info('Prime video started successfully')
        else:
            logO.info('Prime video  startup failed')
        #ѡ��Prime video Home�µĵ�һ������ҳ�ĵ�һ����Ƶ����
        adb.down(3, 1)
        adb.ok(1, 10)
        adb.down(2, 3)
        adb.ok(1, 10)
        adb.down(3)
        adb.left(3)
        #��Prime video ����60S
        adb.ok(1, 60)
    elif random_number == 4:
        result,win = adb.app_start(times=20,keyword='youtube',package='com.google.android.youtube.tv')
        logO.info(win)

        # �ж�YouTube�Ƿ������ɹ�
        if result == True:
            logO.info('YouTube started successfully')
        else:
            logO.info('YouTube  startup failed')
        #����YouTube Home��һ������ҵ�ĵ�һ����Ƶ
        adb.right(1, 3)
        #��YouTube����60S
        adb.ok(1, 60)
        adb.home()
        time.sleep(3)
    else:
        result,win = adb.app_start(times=20,keyword='hungama.Activity.MainActivity',package='com.hungama.movies.tv/com.hungama.Activity.ActivityTermsOfUse')

        # �ж�Hungama�Ƿ������ɹ�
        if result == True:
            logO.info('Hungama started successfully')
        else:
            logO.info('Hungama  startup failed')

        adb.right(1,2)
        adb.ok(1,20)
        result,win = adb.windows('PlayVideoActivity')

        if result == True:
            logO.info('Hungama���ڲ���')
        else:
            logO.info('Hungama����û���ڲ���...')

        # ����60S
        time.sleep(60)
        result, win = adb.windows('PlayVideoActivity')

        if result == True:
            logO.info('Hungama���ڲ���')
        else:
            logO.info('Hungama����û���ڲ���...')

    adb.home()
    time.sleep(3)

    logO.info('��ִ�����' + str(num) + '��')