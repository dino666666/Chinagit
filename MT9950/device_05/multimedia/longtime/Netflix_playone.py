#_*_encoding:GBK*_

import time
import random
import logging
import threading
import queue

from lib.common.adbevent import adb
from lib.common.runinfo import run_log
from lib.common.logcat import log
from device_02.parameter import info

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

#ʵ����һ�����У�ʵ�����߳���������֮���ͨѶ
q=queue.Queue()
thread_two = queue.Queue()

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
    #�ж��Ƿ���Ҫ�˳��ű�ִ��
    text = adb.order('logcat -v time')
    read = text.readline()
    number = 0
    flag = 0

    while read:
        if not q.empty():
            if q.get() == 'q':
                # �������нű�ʱ���ر�logcat��ץȡ
                log.close()
                logO.info('END')
                q.put('q')
                time.sleep(5)
                break

        if not thread_two.empty():
            if thread_two.get() == 'q':
                print('break')
                thread_two.queue.clear()
                time.sleep(2)
                break

        if 'state=2,' in read and flag == 0:
            print(read)
            time.sleep(10)
            adb.ok()
            flag = 1
            number = 0

        if flag == 1:
            number += 1

            if number >= 300:
                flag = 0

        read = text.readline()

#script execution
logO.info('script execution')
time.sleep(2)

#��ʼ���߳�1
thread_thred1 = threading.Thread(target=thread1)
#���߳�1
thread_thred1.start()
#��ʼ���߳�2
thread_thred2 = threading.Thread(target=thread2)
#���߳�2
thread_thred2.start()
#��־λ,Ϊ1ʱ����ѭ��
flag = 0
#����ץȡlogcat
log.open('Netflix_playone')

while True:
    adb.up(3,1)
    adb.ok(5,5)

    for i in range(60):
        result,win = adb.windows('netflix')
        logO.info(win)

        if i % 10 ==0:
            adb.ok()

        if result == True:
            logO.info('��ǰ���洦��Netflix')
        else:
            logO.info('��ǰ���治��Netflix��')
            logO.info('������������Netflix������')
            time.sleep(3)
            # ����Netflix
            result, win = adb.app_start(times=25, keyword='netflix', package='com.netflix.ninja/.MainActivity')
            logO.info(win)

            # �ж�Netflix�Ƿ������ɹ�
            if result == True:
                logO.info('Netflix started successfully')
            else:
                logO.info('Netflix startup failed')

            adb.down(2, 2)
            adb.ok(6, 8)

        #�ж��Ƿ���Ҫ����ѭ�������������еĽű�
        if not q.empty():
            if q.get() == 'q':
                # �������нű�ʱ���ر�logcat��ץȡ
                log.close()
                logO.info('END')
                q.put('q')
                flag=1
                time.sleep(5)
                break
        time.sleep(60)

    thread_two.put('q')
    time.sleep(5)
    # ��ʼ���߳�2
    thread_thred2 = threading.Thread(target=thread2)
    # ���߳�2
    thread_thred2.start()

    state = 3
    if flag == 1:
        break

