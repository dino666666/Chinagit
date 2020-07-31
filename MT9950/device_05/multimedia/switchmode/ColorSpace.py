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
from device_07.parameter import info

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
adb.order('logcat -c',type=1)
logO.info('logcat -c')

#��ʼ���߳�
thread_thred = threading.Thread(target=thread)
#���߳�
thread_thred.start()

#����һ�����֣�����ѭ������
num=0

log.open('color')

while True:
    num += 1
    for i in range(6):
        for ti in range(3):
            adb.menu(num=1,times=5,type=1)
            result,window = adb.windows('com.android.tv.settings')
            if result == True:
                logO.info('Settings started successfully')
                break
            else:
                logO.info('Settings startup failed')
        adb.down(2,1)
        adb.ok(1,2)
        adb.down(2,1)
        adb.ok(1,2)
        adb.down(1,2)
        adb.ok(1,2)

        adb.down(i,1)
        adb.ok(1,2)
        for i in range(3):
            result, window = adb.windows('videoplayer')
            if result == True:
                break
            else:
                adb.back(1)

    result, window = adb.windows('videoplayer')
    if result == True:
        logO.info('videoplayer started successfully')
    else:
        logO.info('videoplayer startup failed')
        adb.ok(2)
    adb.ok()
    time.sleep(3)
    logO.info('��ִ�����' + str(num) + '��')
