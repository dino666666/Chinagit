#_*_encoding:GBK*_
import time
import random
import logging
import threading
import queue

from lib.common.adbevent import adb
from lib.common.runinfo import run_log
from lib.common.logcat import log
from lib.common.initialize import initialize
from device_05.parameter import info
# ����һ�����У�ʵ�����߳���������֮���ͨѶ
q = queue.Queue()
w = queue.Queue()

#����һ���̣߳������ж��Ƿ��Դ���FileBrowser���棬����������������FileBrowser
def thread1():

    while True:
        if not w.empty():
            rights = int(w.get())
            print(rights)
            logO.info('�����쳣��������...')
            initialize(device=device)
            # ����FileBlowser
            result, win = adb.app_start(times=3, keyword='filebrowser',
                                        package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')

            # �ж�FileBrowser�Ƿ������ɹ�
            if result == True:
                logO.info('FileBrowser started successfully')
            else:
                logO.info('FileBrowser startup failed')

            adb.right(rights,2)
            w.queue.clear()

        time.sleep(5)

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

#��ʼ��
initialize(device=device)

#���нű�ǰ�������ʷlogcat
adb.order('logcat -c')
logO.info('logcat -c')

#����FileBlowser
result,win = adb.app_start(times=3,keyword='filebrowser',
                           package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
#�ж�FileBrowser�Ƿ������ɹ�
if result == True:
    logO.info('FileBrowser started successfully')
else:
    logO.info('FileBrowser startup failed')

# #��ʼ���߳�1
# thread_thred1 = threading.Thread(target=thread1)
# #���߳�
# thread_thred1.start()
#��ʼ���߳�2
thread_thred2 = threading.Thread(target=thread2)
#���߳�2
thread_thred2.start()

#��logcat��ģ������ΪFileBrowser
log.open('FileBrowser_VIA')

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

    adb.ok(1,2)

    error = 0
    # ����3����Ƶ
    for i in range(3):
        adb.right(i,1)
        adb.ok(1,5)
        #��ȡ��ǰ�Ӵ���Ϣ
        result,win = adb.windows('videoplayer.playcontrol')

        # �ж���û�н��벥�Ž���
        if result == True:
            logO.info('��Ƶ���ڲ���...')
            time.sleep(60)
            result, win = adb.windows('videoplayer.playcontrol')

            if result == True:
                logO.info('��Ƶ���ڲ���...')
            else:
                logO.info('��Ƶû���ڲ���...')
                error = 1
                break
        else:
            logO.info('��Ƶû���ڲ���...')
            error = 1
            break

        adb.back(1,2)

    # �쳣����
    if error == 1:
        w.put('0')
        time.sleep(30)
        error = 0
    else:
        adb.back(1,2)

    # ����10��ͼƬ
    adb.right(1,2)
    adb.ok(5,1)

    for i in range(10):
        # �ж���û���ڲ���ͼƬ
        result,win = adb.windows('gallery3d')
        logO.info(win)

        if result == True:
            logO.info('���ڲ���ͼƬ...')
        else:
            logO.info('ͼƬû���ڲ���...')
            error = 1
            break

        adb.right(1,5)

    # �쳣����
    if error == 1:
        w.put('temp')
        time.sleep(30)
        error = 0
    else:
        adb.back(3, 2)

    # ����3����Ƶ
    adb.right(1,2)
    adb.ok(1,2)

    for i in range(3):
        adb.down(i,2)
        adb.ok(1,5)
        result,win = adb.windows('musicplayer')
        logO.info(win)

        if result ==True:
            logO.info('��Ƶ���ڲ���...')
        else:
            logO.info('��Ƶû���ڲ���...')
            error = 1
            break

        time.sleep(30)

        result, win = adb.windows('musicplayer')
        logO.info(win)

        if result == True:
            logO.info('��Ƶ���ڲ���...')
        else:
            logO.info('��Ƶû���ڲ���...')
            error = 1
            break

        adb.back(1,2)

    # �쳣����
    if error == 1:
        w.put('2')
        time.sleep(30)
        error = 0
    else:
        adb.back(1, 2)

    adb.left(5,1)

    logO.info('��ִ�����'+str(num)+'��')