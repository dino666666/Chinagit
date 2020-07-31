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

    # ��logcat��ģ������ΪFileBrowser
    log.open('FileBrowser')
    # ����FileBlowser
    result, win = adb.app_start(times=3, keyword='filebrowser',
                                package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
    # �ж�FileBrowser�Ƿ������ɹ�
    if result == True:
        logO.info('FileBrowser started successfully')
    else:
        logO.info('FileBrowser startup failed')
    # ѡ��Video
    adb.left(3, 1)
    adb.ok(1, 2)
    random_number = random.randint(1,9)
    event = random_number%3

    if event == 1:
        adb.down(random_number)
        adb.ok()
    elif event == 2:
        adb.right(random_number)
        adb.ok()
    else:
        adb.ok()
    #����30S
    time.sleep(30)
    logO.info('��ִ�����' + str(num) + '��')

    if num%10==0:
        adb.back(5,1)
        #�жϷ��ؽ��Ƿ���Ч
        result, window = adb.windows('com.google.android.tvlauncher')
        logO.info(window)

        if result == True:
            logO.info('���ؼ���Ч')
        else:
            logO.info('���ؼ���Ч')