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

#����һ���̣߳������ж��Ƿ��Դ���FileBrowser���棬����������������FileBrowser
def thread1():
    li = ['filebrowser','gallery3d','playcontrol','musicplayer','null']
    flag = 0

    while True:
        result,window = adb.windows(' ')
        for i in li:
            if i in window:
                flag = 1
                break

        if flag == 0:
            adb.app_start(package='com.oneplus.tv.filebrowser/.ui.activity.MainActivity')
        time.sleep(2)
        logO.info(window)
        flag=0

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

#��ʼ���߳�1
thread_thred1 = threading.Thread(target=thread1)
#���߳�
thread_thred1.start()
#��ʼ���߳�2
thread_thred2 = threading.Thread(target=thread2)
#���߳�2
thread_thred2.start()

#��logcat��ģ������ΪFileBrowser
log.open('FileBrowser')

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

    #���۽���Video������Audio����ѭ��3��
    for i in range(3):
        adb.left(4)
        # �����漴�����������Video��Image��Audio����ѡ��
        number = random.randint(0,2)
        adb.right(number)
        adb.ok(1,1)
        #��ȡ��ǰ�Ӵ��������жϽ���Video������Audio
        result,window = adb.windows(' ')

        if 'com.oneplus.tv.filebrowser.ui.activity.ContentActivity' in window:
            #��Videoѭ��3��
            for o in range(3):
                #���������
                number = random.randint(1,8)
                #�����������������¼���������б�ѡ������һ�����ţ���Ƶ�������֣�
                event = number%4
                if number > 4:
                    adb.right(event)
                else:
                    adb.down(event)
                adb.ok(1,1)
                result, window = adb.windows(' ')

                #�жϲ��ŵ�����Ƶ������Ƶ
                if 'videoplayer.playcontrol' in window:
                    logO.info('������Ƶ���š���')
                    logging.debug('videoplayer.playcontrol')
                    #�жϲ��ŵ�����Ƶʱ��ִ����������¼�
                    number = random.randint(0,8)
                    event = number%4
                    if number > 4:
                        adb.right(event)
                    else:
                        adb.left(event)
                    adb.ok(event,number)
                elif 'com.oneplus.tv.musicplayer.activity.MainActivity' in window:
                    logO.info('������Ƶ���š���')
                    #�жϲ��ŵ�����Ƶʱ��ִ����������¼�
                    number = random.randint(0,8)
                    event = number%3

                    if event == 1:
                        logging.debug('music1')
                        adb.left(1,1)
                        adb.ok(1,3)
                        adb.right()
                    elif event == 2:
                        logging.debug('music2')
                        adb.right(1,1)
                        adb.ok(1,3)
                        adb.left()
                    else:
                        logging.debug('music else')
                        adb.up(2,1)

                        if number > 4:
                            for i in range(event):
                                adb.left(type=1)
                        else:
                            for i in range(event):
                                adb.right(type=1)
                        adb.down(1,10)

                else:
                    break
        #�жϵ�ǰ�Ƿ���Image
        elif 'com.android.gallery3d.app.Gallery' in window:
            logO.info('����ͼƬ����')
            #����������������󻬻����ֻ�
            number = random.randint(0,4)
            adb.right(number)
            adb.ok(1,1)
            number = random.randint(0, 6)
            adb.right()
            adb.ok(1,1)
            number = random.randint(0, 1)

            for i in range(0,3):

                if number == 1:
                    adb.left(type=1)
                else:
                    adb.right(type=1)
                time.sleep(3)

            adb.ok(2)
        else:
            pass

        logging.debug('��ʼ����..')
        adb.back(2,1)

        #���ص�Video��Audio��Imageѡ��
        for i in range(3):
            result,window=adb.windows('com.oneplus.tv.filebrowser.ui.activity.MainActivity')

            if result == True:
                break
            else:
                adb.back(1,1)
