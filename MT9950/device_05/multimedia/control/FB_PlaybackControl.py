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
w=queue.Queue()
#����һ���̣߳������ж��Ƿ��Դ���FileBrowser���棬����������������FileBrowser
def thread1():
    time.sleep(30)
    while True:

        if not w.empty():
            if w.get() == 'check_p':
                for i in range(5):
                    print(i)
                    time.sleep(2)
                adb.ok()
                w.queue.clear()

        result,window = adb.windows('videoplayer.playcontrol')

        if result == False:
            w.put('p')
            adb.home(1,1)
            adb.app_start(times=3,package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
            adb.left(3,1)
            adb.ok(2,2)
        time.sleep(2)
        logO.info(window)

        if not q.empty():
            if q.get() == 'q':
                logO.info('END')
                q.put('q')
                break

def thread2():
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

#��ʼ���߳�1
thread_thred1 = threading.Thread(target=thread1)
#���߳�
thread_thred1.start()
#��ʼ���߳�2
thread_thred2 = threading.Thread(target=thread2)
#���߳�2
thread_thred2.start()

#��logcat��ģ������ΪPlaybackControl
log.open('PlaybackControl')

# ����FileBlowser
result, win = adb.app_start(times=3, keyword='filebrowser',
                            package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
# �ж�FileBrowser�Ƿ������ɹ�
if result == True:
    logO.info('FileBrowser started successfully')
else:
    logO.info('FileBrowser startup failed')

#ѡ��Video
adb.left(3,1)
adb.ok(2,2)
#����һ�����֣�����ѭ������
num=0

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
    #����������������ǲ�����Ƶ�����Ƿ�����Ƶ�б�����ѡ��һ����Ƶ����
    random_number = random.randint(1,12)
    event = random_number%3
    logO.info('event:'+str(event))

    if event != 0:
        number = 0

        for i in range(10):
            #�����������������������ȡ���ͣ������
            random_number = random.randint(1,12)
            event = random_number%4

            if random_number > 7:
                adb.right(event)
            else:
                adb.left(event)

            if random_number%4 == 0:
                adb.ok()
                number += 1
                print('number:',number)

            if not w.empty():
                if w.get() == 'p':
                    # �������нű�ʱ���ر�logcat��ץȡ
                    time.sleep(10)
                    w.queue.clear()
                    number=1
                    break
        #���ؽ����󣬲���30S
        if number%2 == 1:
            adb.ok()
        else:
            pass
        time.sleep(30)
    else:
        w.put('check_p')
        adb.back()
        time.sleep(2)

        if event%5 == 1:
            adb.right(random_number)
            adb.ok()
        elif event%5 == 2:
            adb.down(random_number)
            adb.ok()
        elif event%5 == 3:
            adb.up(random_number)
            adb.ok()
        elif event%5 == 4:
            adb.left(random_number)
        else:
            adb.ok()

    #ÿִ��10������¼�����������Ƶ�б����ѡ����Ƶ����
    if num%10 == 0:
        w.put('check_p')
        adb.back(1,2)
        if event % 5 == 1:
            adb.right(random_number)
            adb.ok()
        elif event % 5 == 2:
            adb.down(random_number)
            adb.ok()
        elif event % 5 == 3:
            adb.up(random_number)
            adb.ok()
        elif event % 5 == 4:
            adb.left(random_number)
        else:
            adb.ok()

    logO.info('��ִ�����' + str(num) + '��')