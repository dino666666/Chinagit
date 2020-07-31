#_*_encoding:GBK*_
#�����������������Ļ���

import os
import time
import logging
import threading
import queue

# ��
from lib.common.adbevent import adb
from lib.common.runinfo import run_log
from lib.common.logcat import log
# ����
from lib.common.initialize import initialize
from lib.common.template_matching import compare
from device_05.parameter import info

#��ʼ���豸��Ϣ�Լ��ű����й����в������ļ�����·��
device,path = info()
#����ű����й����в������ļ�·��
logpath = path + 'log/'
picturepath = path + 'picture/'
runpath = path + 'runinfo/'

# ��������
q=queue.Queue()
w=queue.Queue()
key=queue.Queue()
app=queue.Queue()

#ʵ����
#������Ϣ
logO = run_log(logging_path=runpath,logger=device).getlog()
#�豸��Ϣ
adb = adb(device=device)
#logcat��Ϣ
log = log(log_path=logpath,device=device)

#�ű�������Ϣ
logging.basicConfig(level=logging.DEBUG,format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

def thread1():
    #�ж��Ƿ���Ҫ�˳��ű�ִ��
    while True:
        end = input('������q��������:')
        if end == 'q':
            q.put('q')
            break

        if not q.empty():
            if q.get() == 'q':
                q.put('q')
                time.sleep(2)
                logO.info('END')
                break

def thread2():
    text = adb.order('logcat -v time')
    read = text.readline()
    number = 0
    keyword = None
    flag = 0

    while read:
        if not q.empty():
            if q.get() == 'q':
                logO.info('END')
                q.put('q')
                break

        if not key.empty():
            keyword = key.get()
            logging.debug(keyword)
            flag = 1
            key.queue.clear()
            T0 = time.time()

        if flag == 1:
            number += 1
            if number % 100 == 0:
                T1 = time.time()
                T = T1 - T0

                if T >= 6:
                    w.put('none')
                    logging.debug('none')
                    logO.info(read)
                    flag = 0
                    number = 0

            if keyword in read:
                w.put('p')

        read = text.readline()

def thread3():
    while True:
        if not q.empty():
            if q.get() == 'q':
                q.put('q')
                time.sleep(2)
                logO.info('END')
                break

        time.sleep(2)
        if not app.empty():
            if app.get() == 'error':
                adb.back(5)
                time.sleep(1)
                adb.menu()
                time.sleep(3)
                adb.left(7)
                time.sleep(1)
                adb.ok(1,3)
                adb.left(9)
                key.put('HDMI1')
                adb.ok(1,3)
                logO.info('�쳣����...')

                if w.get() == 'none':
                    logO.info('����ʧ��!')
                    logO.info('��ǰsource������HDMI1')
                    adb.app_stop(times=3,package='com.oneplus.tv.android.livetv')
                    result, win = adb.app_start(times=3, keyword='livetv',
                                                package='com.oneplus.tv.android.livetv/.ActivityEntrance')
                    logO.info(win)

                    # �ж�Live TV�Ƿ������ɹ�
                    if result == True:
                        logO.info('Live TV started successfully')
                    else:
                        logO.info('Live TV startup failed')

                    adb.down(3)
                    adb.ok(1,5)
                    adb.menu()
                    adb.left(5)
                    adb.ok(1,3)
                    adb.left(9)
                    key.put('HDMI1')
                    adb.ok(1,3)
                    logO.info('�ٴγ����쳣����...')

                    if w.get() == 'none':
                        logO.info('����ʧ��!')
                        logO.info('��ǰsource������HDMI1')
                        logO.info('�����쳣���������нű�...')
                    else:
                        pass
                else:
                    logO.info('����ɹ�')
                    logO.info('��ǰsource����HDMI1')

            app.queue.clear()

#script execution
logO.info('script execution')
time.sleep(2)

#��ʼ��
initialize(device=device)
time.sleep(2)

#���нű�ǰ�������ʷlogcat
adb.order('logcat -c')
logO.info('logcat -c')
time.sleep(2)
log.open('SS_HDMI')

#��ʼ���߳�1
thread_thred1 = threading.Thread(target=thread1)
#���߳�1
thread_thred1.start()
#��ʼ���߳�2
thread_thred2 = threading.Thread(target=thread2)
#���߳�2
thread_thred2.start()
#��ʼ���߳�3
thread_thred3 = threading.Thread(target=thread3)
#���߳�3
thread_thred3.start()

#���ݹؼ��֣������ж��Ƿ���HDMI1
key.put('HDMI1')
time.sleep(2)
result,win = adb.app_start(times=3,keyword='livetv',
                           package='com.oneplus.tv.android.livetv/.ActivityEntrance')
logO.info(win)

# �ж�Live TV�Ƿ������ɹ�
if result == True:
    logO.info('Live TV started successfully')
else:
    logO.info('Live TV startup failed')

num=0

while True:

    if num == 0:
        if w.get() == 'none':
            logO.info('��ǰsource����HDMI1��������ű�ִ������...')
            logO.info('�����˳��ű�����...')
            q.put('q')
        else:
            logO.info('��ǰsource ����HDMI1,����ű�ִ������')
            logO.info('�ű�����ִ��...')
            w.queue.clear()

    # �ж��Ƿ���Ҫ����ѭ�������������еĽű�
    if not q.empty():
        if q.get() == 'q':
            q.put('q')
            time.sleep(2)
            # �������нű�ʱ���ر�logcat��ץȡ
            log.close()
            logO.info('END')
            break

    # ÿ��ѭ��num+temp
    num += 1
    # д��������Ϣ
    logO.info('��ʼִ�е�' + str(num) + '��')

    # �л���HDMI2
    adb.menu()
    time.sleep(3)
    adb.ok(1,2)
    adb.right(1,2)
    #����log�ؼ���HDMI2�ж��Ƿ����HDMI2
    key.put('HDMI2')
    adb.ok(1,2)

    if w.get() == 'none':
        logO.info('��ǰsource������HDMI2')
    else:
        logO.info('��ǰsource����HDMI2')

    w.queue.clear()
    # ��HDMI2�в���10S
    time.sleep(10)
    # �л���HDMI3
    adb.menu()
    time.sleep(3)
    adb.ok(1, 2)
    adb.right(1, 2)
    # ����log�ؼ���HDMI3�ж��Ƿ����HDMI3
    key.put('HDMI3')
    adb.ok(1, 2)

    if w.get() == 'none':
        logO.info('��ǰsource������HDMI3')
    else:
        logO.info('��ǰsource����HDMI3')

    w.queue.clear()
    # ��HDMI3�в���10S
    time.sleep(10)
    # �л���HDMI4
    adb.menu()
    time.sleep(3)
    adb.ok(1, 2)
    adb.right(1, 2)
    # ����log�ؼ���HDMI4�ж��Ƿ����HDMI4
    key.put('HDMI4')
    adb.ok(1, 2)

    if w.get() == 'none':
        logO.info('��ǰsource������HDMI4')
    else:
        logO.info('��ǰsource����HDMI4')

    w.queue.clear()
    # ��HDMI4�в���10S
    time.sleep(10)
    # �л���HDMI1
    adb.menu()
    time.sleep(3)
    adb.ok(1, 2)
    adb.left(6)
    # ����log�ؼ���HDMI2�ж��Ƿ����HDMI2
    key.put('HDMI1')
    adb.ok(1, 2)

    if w.get() == 'none':
        logO.info('��ǰsource������HDMI1')
        #�жϽű�ִ���쳣�������쳣��������
        app.put('error')
        time.sleep(60)
    else:
        logO.info('��ǰsource����HDMI1')

    w.queue.clear()
    # ��HDMI2�в���10S
    time.sleep(10)
    logO.info('��ִ�����' + str(num) + '��')
    time.sleep(3)
