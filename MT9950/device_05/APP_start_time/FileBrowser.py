#_*_encoding:GBK*_

import os
import time
import logging
import threading
import queue

# ��
from lib.common.adbevent import adb
from lib.common.runinfo import run_log
from lib.common.logcat import log
from lib.common.BasePage import Basepage
from lib.common.part_image import template_part
from appium.webdriver.common.mobileby import MobileBy
# ����
from lib.common.initialize import initialize
from lib.common.template_matching import compare
from device_01.parameter import info

#��ʼ���豸��Ϣ�Լ��ű����й����в������ļ�����·��
device,path = info()
#����ű����й����в������ļ�·��
logpath = path + 'log/'
picturepath = path + 'picture/'
runpath = path + 'runinfo/'

# ��������
q=queue.Queue()

#ʵ����
#������Ϣ
logO = run_log(logging_path=runpath,logger=device).getlog()
#�豸��Ϣ
adb = adb(device=device)
#logcat��Ϣ
log = log(log_path=logpath,device=device)

#�ű�������Ϣ
logging.basicConfig(level=logging.DEBUG,format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

def thread():
    #�ж��Ƿ���Ҫ�˳��ű�ִ��
    while True:
        end = input('������q��������:')
        if end == 'q':
            q.put('q')
            break

#��ʼ���߳�
thread_thred1 = threading.Thread(target=thread)
#���߳�
thread_thred1.start()

num = 0

while True:
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
    flag = 0
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

    adb.screencap(path=picturepath, type=1, module='WiFi_routine_' + str(num) + '_')
    time.sleep(3)

    # �ж��������Ƿ���Google Lanucher
    result, window = adb.windows('com.google.android.tvlauncher')
    logO.info(window)

    if result == True:
        logO.info('��ǰ���洦��Google Lanucher')
    else:
        logO.info('��ǰ���治����Google Lanucher')
        adb.screencap(path=picturepath, type=1, module='AC_' + str(num) + '_')
    # ��logcat
    log.open('Reboot')

    command = 'adb -s ' + device + ' am start -W com.oneplus.tv.filebrowser/.ui.activity.MainActivity'
    result = os.popen(command)
    result_read = result.readline()
    while result_read:

        result_read = result.readline()