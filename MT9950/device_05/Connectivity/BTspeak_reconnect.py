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

# ����һ������
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

#script execution
logO.info('script execution')
time.sleep(2)

#��ʼ��
initialize(device=device)
time.sleep(2)
adb.order('rm -rf /sdcard/*.png')

#��ʼ���߳�
thread_thred = threading.Thread(target=thread)
#���߳�
thread_thred.start()

#���нű�ǰ�������ʷlogcat
adb.order('logcat -c')
logO.info('logcat -c')

time.sleep(2)
result,win = adb.app_start(times=25,keyword='btspeaker',
                           package='com.oneplus.tv.btspeaker/.MainActivity')
logO.info(win)

# �ж�Bluetooth Stereo�Ƿ������ɹ�
if result == True:
    logO.info('Bluetooth Stereo started successfully')
else:
    logO.info('Bluetooth Stereo startup failed')

template_name = picturepath+'template.png'
# ����
adb.screencap(path=template_name)
time.sleep(2)
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

    # ��logcat��ģ������ΪBTspeak
    log.open('BTspeak')
    result, win = adb.app_start(times=15, keyword='btspeaker',
                               package='com.oneplus.tv.btspeaker/.MainActivity')
    logO.info(win)

    # �ж�Bluetooth Stereo�Ƿ������ɹ�
    if result == True:
        logO.info('Bluetooth Stereo started successfully')
    else:
        logO.info('Bluetooth Stereo startup failed')

    # ɾ��/sdcard�µ�����.png�ļ�
    adb.order('rm -rf /sdcard/*.png')
    # ��ȡ��ǰʱ�䲢��ʽ��
    pt = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    picture_name = picturepath+'BTspeak'+pt+'.png'
    #��ͼ
    adb.screencap(path=picture_name)
    time.sleep(2)
    judge = os.path.exists(picture_name)

    # ���PC�����Ƿ������Ҫ�Աȵ�ͼ��
    if judge == True:
        logO.info('��ʼ����ͼ��ȶ�...')

        # ��ʼ����ͼ��ȶԣ�pass��ͼƬɾ����fail����
        if compare(picture1=template_name,picture2=picture_name,value=0.99):
            logO.info('pass')
            time.sleep(1)
            os.remove(picture_name)#ɾ��pass��ͼƬ
        else:
            logO.info('fail')
            logO.info('30S���ٳ���һ��...')
            time.sleep(30)
            # ɾ��/sdcard�µ�����.png�ļ�
            adb.order('rm -rf /sdcard/*.png')
            # ��ȡ��ǰʱ�䲢��ʽ��
            pt = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            picture_name = picturepath + 'BTspeak' + pt + '.png'
            # ��ͼ
            adb.screencap(path=picture_name)
            time.sleep(2)
            judge = os.path.exists(picture_name)

            # ���PC�����Ƿ������Ҫ�Աȵ�ͼ��
            if judge == True:
                logO.info('��ʼ����ͼ��ȶ�...')

                # ��ʼ����ͼ��ȶԣ�pass��ͼƬɾ����fail����
                if compare(picture1=template_name, picture2=picture_name,value=0.99):
                    logO.info('pass')
                    time.sleep(1)
                    os.remove(picture_name)  # ɾ��pass��ͼƬ
                    logO.info('��ִ�����' + str(num) + '��')

            else:
                logO.info('30S Fail')
    else:
        time.sleep(2)
        initialize(device=device)
        time.sleep(10)

    logO.info('��ִ�����' + str(num) + '��')
    time.sleep(3)