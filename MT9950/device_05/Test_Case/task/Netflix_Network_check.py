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
from device_01.parameter import info
from lib.tools.camera_cap import picture

#ʵ����һ�����У�ʵ�����߳���������֮���ͨѶ
q=queue.Queue()

def thread():
    #�ж��Ƿ���Ҫ�˳��ű�ִ��
    while True:
        end = input('������q��������:')
        if end == 'q':
            q.put('q')
            break

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

#���нű�ǰ�������ʷlogcat
adb.order('logcat -c')
logO.info('logcat -c')

#��ʼ���߳�
thread_thred = threading.Thread(target=thread)
#���߳�
thread_thred.start()

#����һ�����֣�����ѭ������
num=0

while True:
    flag = 0
    # �ж��Ƿ���Ҫ����ѭ�������������еĽű�
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
    adb.oneplus(type=1)
    adb.left(3, 1)
    adb.ok()
    # ��ȡ��ǰʱ��
    T0 = time.time()
    time.sleep(8)
    # ��鵱ǰ�Ӵ�
    result, win = adb.windows('com')
    logO.info(result)
    logO.info(win)

    # �����Ӵ���Ϣ���ж�TV�Ƿ�����������������ָ��reboot����
    if result == True:
        adb.order('reboot')
        T0 = time.time()

    # ÿ��0.3S���һ�ε�ǰ�Ӵ����ж�TV�Ƿ��Ѿ��������
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
        logO.info('�����ɹ�')
    else:
        logO.info('����ʧ��')

    # ��������ʱ�䣬���
    T = T1 - T0
    logO.info('������ʱ:' + str(T) + 'S')

    time.sleep(10)
    # �ж��������Ƿ���Google Lanucher
    result, window = adb.windows('com.google.android.tvlauncher')
    logO.info(window)

    if result == True:
        logO.info('��ǰ���洦��Google Lanucher')
    else:
        logO.info('��ǰ���治����Google Lanucher')

    # ��logcat��ģ������ΪNetflix_Network_check
    log.open('Netflix_Network_check')
    time.sleep(30)
    adb.netflix()
    time.sleep(30)
    result,win = adb.windows('netflix')
    logO.info(win)

    # �ж�Netflix�Ƿ������ɹ�
    if result == True:
        logO.info('Netflix started successfully')
    else:
        logO.info('Netflix startup failed')
        time.sleep(5)

    adb.order(' logcat -c ', type=1)
    time.sleep(3)
    adb.ok(2,30)
    adb.ok(1,5)
    # order = 'adb -s ' + device_05 + 'logcat'
    logcat = os.popen('adb -s 001AAAAJC100152BA8 logcat')

    read = logcat.readline()
    # time.sleep(10)
    flag_network_check = 0
    num_network_check = 0
    while read:
        # print(read)
        if 'NewAvrcpMediaPlayerWrapper' in read and 'com.netflix.ninja' in read:
            print('True')
            print(read)
            flag_network_check = 1
            break


        if num_network_check >= 1000:
            break
        elif num_network_check % 200 == 0:
            result, win = adb.windows('netflix')
            logO.info(win)

            # �ж�Netflix�Ƿ������ɹ�
            if result == True:
                logO.info('Netflix started successfully')
            else:
                logO.info('Netflix startup failed --try')
                adb.netflix()
                adb.ok(5, 3)
        num_network_check += 1
        print(num_network_check)

        read = logcat.readline()
    picture(path='/home/oneplus/IndiaData/log/')
    # �ж�Netflix Network
    if flag_network_check == 1:
        logO.info('Netflix Network check Pass')
    else:
        logO.info('Netflix Network check Fail')
        for i in range(3):
            picture(path='/home/oneplus/IndiaData/log/')
            time.sleep(3)
    time.sleep(5)