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
log.open('FB_BTspeak')

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

    # ����FileBlowser
    result, win = adb.app_start(times=3, keyword='filebrowser',
                                package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
    logO.info(win)

    # �ж�FileBrowser�Ƿ������ɹ�
    if result == True:
        logO.info('FileBrowser started successfully')
    else:
        logO.info('FileBrowser startup failed')

    # ѡ��Video
    adb.left(3, 1)
    adb.ok(2, 2)

    # ����60S
    for i in range(3):
        result,win = adb.windows('videoplayer.playcontrol')
        logO.info(win)

        if result == True:
            logO.info('��Ƶ���ڲ���...')
        else:
            logO.info('��Ƶû���ڲ���...')

        time.sleep(20)

    adb.back(5)
    #����Bluetooth Stereo
    result, win = adb.app_start(times=3, keyword='btspeaker',
                                package='com.oneplus.tv.btspeaker/.MainActivity')
    logO.info(win)

    # �ж�Bluetooth Stereo�Ƿ������ɹ�
    if result == True:
        logO.info('Bluetooth Stereo started successfully')
    else:
        logO.info('Bluetooth Stereo startup failed')

    adb.ok(1,30)
    result,win = adb.windows('btspeaker')
    logO.info(win)

    if result == True:
        logO.info('������Ȼ�ڲ���...')
    else:
        logO.info('����û���ڲ���...')


    adb.home()
    adb.down(6)
    adb.right(6)
    adb.up(5)
    adb.left(5)

    # ����WiFi
    result, win = adb.app_start(times=3, keyword='NetworkActivity',
                                package='com.android.tv.settings/.connectivity.NetworkActivity')
    logO.info(win)

    if result == True:
        logO.info('WiFi started successfully')
    else:
        logO.info('WiFi startup failed')

    adb.ok(1,3)
    adb.left(3)
    adb.ok(1,5)

    # ����FileBlowser
    result, win = adb.app_start(times=3, keyword='filebrowser',
                                package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
    logO.info(win)

    # �ж�FileBrowser�Ƿ������ɹ�
    if result == True:
        logO.info('FileBrowser started successfully')
    else:
        logO.info('FileBrowser startup failed')

    adb.right(6)
    adb.ok(1,2)
    adb.down(5)
    adb.ok(1,5)

    for i in range(3):
        result,win = adb.windows('musicplayer')

        if result == True:
            logO.info('��ǰ��Ƶ���ڲ���...')
        else:
            logO.info('��ǰ��Ƶû���ڲ���...')

        time.sleep(20)

    adb.back(5)

    logO.info('��ִ�����' + str(num) + '��')