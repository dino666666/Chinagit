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

#ʵ����һ�����У�ʵ�����߳���������֮���ͨѶ
q = queue.Queue()
w = queue.Queue()
key = queue.Queue()
system_info = queue.Queue()
thread_o = queue.Queue()

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
                logO.info('��ʼ�����쳣����...')
                initialize(device=device)
                adb.app_stop(times=3, package='com.oneplus.tv.filebrowser')
                # ����FileBrowser
                result, win = adb.app_start(times=3, keyword='filebrowser',
                                            package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
                # �ж�FileBrowser�Ƿ������ɹ�
                if result == True:
                    logO.info('FileBrowser started successfully')
                else:
                    logO.info('FileBrowser startup failed')
                    logO.info('����ʧ�ܣ������쳣��������...')

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
                logO.info('ģʽ�л��ɹ�')
                keynum = 0
                flag = 0

            if keynum >= 100:
                T1 = time.time()
                T = T1 - T0

                if T >= 10:
                    logO.info('ģʽ�л�ʧ��...')
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

#��logcat��ģ������ΪPlaybackControl
log.open('FB_SM')

# ����FileBrowser
result, win = adb.app_start(times=3, keyword='filebrowser',
                            package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
# �ж�FileBrowser�Ƿ������ɹ�
if result == True:
    logO.info('FileBrowser started successfully')
else:
    logO.info('FileBrowser startup failed')

#ѡ��Video
adb.left(3)
adb.ok(2,2)
#����һ�����֣�����ѭ������
num=0
modle = 0
# modle_list = ['Vivid','Custom','Cinema_Pro','Cinema_Home','Photo_Standard','Graphic','Standard']
modle_list = ['Dolby_Vision_Dark','Dolby_Vision_Bright']
while True:
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

    for m in modle_list:
        modle += 1
        print(m)

        for i in range(3):
            result,win = adb.windows('playcontrol')
            logO.info(win)

            if result == True:
                logO.info('��Ƶ���ڲ���')
            else:
                logO.info('��Ƶ����û���ڲ���')
                w.put('p')

            time.sleep(20)

        logO.info('��ʼ�л�ģʽ...')
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
        # ��ʼ���߳�2
        thread_thred2 = threading.Thread(target=thread2)
        # ���߳�2
        thread_thred2.start()
        # ��ʼ���߳�3
        thread_thred3 = threading.Thread(target=thread3)
        # ���߳�3
        thread_thred3.start()

    logO.info('��ִ�����' + str(num) + '��')