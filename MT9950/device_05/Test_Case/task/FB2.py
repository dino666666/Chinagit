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
from lib.common.bright import brightness
from lib.tools.camera_cap import picture
from device_03.parameter import info

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
    command1 = 'adb -s ' + device + ' logcat -c'
    print(command1)
    os.system(command1)
    adb.ok()
    # ��ȡ��ǰʱ��
    T0 = time.time()
    time.sleep(8)
    # ��鵱ǰ�Ӵ�
    result, win = adb.windows('mCurren')
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

    time.sleep(3)
    log.open(module='PQ')

    # ����FileBlowser
    result, win = adb.app_start(times=3, keyword='filebrowser',
                                package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
    # �ж�FileBrowser�Ƿ������ɹ�
    if result == True:
        logO.info('FileBrowser started successfully')
    else:
        logO.info('FileBrowser startup failed')
    # ѡ��Video
    adb.left(2)
    adb.right(2,1)
    adb.ok(1, 2)
    adb.right(2)
    adb.ok(1,5)
    time.sleep(5)

    picture_name = picture(path=picturepath,camera_number=0,mode='PQ')
    logO.info(picture_name)
    value = brightness(picture_name)

    print(value)
    logO.info('value:' + str(value))
    command = 'adb -s ' + device + ' shell getprop | grep -i picture'
    log_get = os.popen(command)
    log_read = log_get.read()
    logO.info(log_read)
    try:
        log_key = log_read.split(':')
        if 'Standard' in log_key[-1]:
            logO.info('PQ Pass')
            print('PASS')
        else:
            logO.info('PQ Fail')
            print('FAIL')
        print(log_key)
    except:
        logO.info('PQ Fail')
        print('FAIL')

    if int(value) >= 100:
        break

    logO.info('��ִ�е�' + str(num) + '��')