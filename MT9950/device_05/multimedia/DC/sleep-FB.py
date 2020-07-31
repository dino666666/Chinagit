#_*_encoding:GBK*_

import time
import logging
import threading
import queue

from lib.common.adbevent import adb
from lib.common.runinfo import run_log
from lib.common.logcat import log
from lib.common.initialize import initialize
from device_05.parameter import info

#����һ�����У�ʵ�����߳���������֮���ͨѶ
q=queue.Queue()
w=queue.Queue()

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

#��ʼ��
initialize(device=device)

#���нű�ǰ�������ʷlogcat
adb.order('logcat -c')
logO.info('logcat -c')


def thread1():
    # �ж��Ƿ���Ҫ�˳��ű�ִ��
    while True:
        end = input('������q��������:')
        if end == 'q':
            q.put('q')
            break

def thread2():
    # �ж��Ƿ����˳�FileBrowser
    while True:
        time.sleep(2)

        if not w.empty():

            if w.get() == 'p':
                # �ص�FileBrowser�������½���Video������Ƶ
                adb.app_stop(times=2,package='com.oneplus.tv.filebrowser')
                adb.app_start(times=3,keyword='filebrowser',
                              package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
                adb.left(3,1)
                adb.ok(2,2)

                w.queue.clear()

        if not q.empty():
            if q.get() == 'q':
                logO.info('END')
                q.put('q')
                break

#��ʼ���߳�1
thread_thred1 = threading.Thread(target=thread1)
#���߳�1
thread_thred1.start()
#��ʼ���߳�2
thread_thred2 = threading.Thread(target=thread2)
#���߳�2
thread_thred2.start()

#����һ�����֣�����ѭ������
num=0

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

while True:
    flag=0
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
    adb.ok(1,2)
    time.sleep(3)
    result,win = adb.windows('playcontrol')
    logO.info(result)
    logO.info(win)

    if result == True:
        logO.info('���ڲ�����Ƶ����')
    else:
        logO.info('��Ƶû���ڲ���')
        adb.ok(1,3)
        result, win = adb.windows('playcontrol')
        logO.info(result)
        logO.info(win)

        if result == False:
            logO.info('��Ƶû���ڲ���-�����ٴβ���')
            w.put('p')
            time.sleep(30)

    adb.oneplus(type=1)

    for i in range(3):
        result,win=adb.windows('ActionsDialog')

        if result == True:
            pass
        else:
            adb.right(1,2)
            adb.oneplus(type=1)
            break
    adb.ok(1,15)
    adb.oneplus()

    logO.info('��ִ�����' + str(num) + '��')
    time.sleep(3)
