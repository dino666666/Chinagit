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
log.open('cast')

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
    applist = ['com.google.android.youtube.tv','com.graymatrix.did/com.zee5.splash.SplashActivity','com.netflix.ninja/.MainActivity',
               'com.amazon.amazonvideo.livingroom/com.amazon.ignition.IgnitionActivity','com.oneplus.tv.filebrowser/.ui.activity.MainActivity',
               'com.hungama.movies.tv/com.hungama.Activity.ActivityTermsOfUse']

    random_number = random.randint(0, 6)

    if random_number <= 5:
        adb.app_start(times=3, package=applist[random_number])
    else:
        adb.home()

    for i in range(30):
        time.sleep(3)
        result, win = adb.windows('apps.mediashell')
        logO.info(win)

        if result == True:
            break

    result,win = adb.windows('apps.mediashell')
    if result == True:
        logO.info('Ͷ���ɹ�')
        time.sleep(5)
        adb.back(1,60)
    else:
        logO.info('û��Ͷ��')

    if random_number <=5:
        result,win = adb.windows(applist[random_number])
        logO.info(win)
        if result == True:
            logO.info('��Ȼ��ԭ����...')
        else:
            logO.info('�Ѳ���ԭ����...')