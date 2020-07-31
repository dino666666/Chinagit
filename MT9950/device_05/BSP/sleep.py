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
# from lib.common.BasePage import Basepage
from lib.common.part_image import template_part
# ����
# from lib.common.initialize import initialize
# from lib.common.template_matching import compare
from device_05.parameter import info

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

log.open(module='STR')
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

    adb.oneplus(type=1)
    result,window = adb.windows('ActionsDialog')
    if result == True:
        adb.ok()
    else:
        adb.order('input keyevent KEYCODE_POWER')

    time.sleep(5)

    try:
        name = adb.screencap(path=picturepath, module='Sleep', type=1)
        judge = os.path.exists(name)
        # ���PC�����Ƿ������Ҫ�Աȵ�ͼ��
        if judge == True:
            logO.info('====��ʼ����ͼ��ȶ�====')
            wifi_picture = picturepath + 'Setting.png'
            result, coordinate = template_part(wifi_picture, name,num=0.64)

            # ��ʼ����ͼ��ȶԣ�pass��ͼƬɾ����fail����
            if result == False:
                logO.info('Setting logo fail')
                logO.info(' Sleep pass')
                time.sleep(1)
                # ɾ��pass��ͼƬ
                os.remove(name)
            else:
                logO.info('Setting logo pass')
                logO.info('Sleep fail')
                logO.info('�ٳ��Լ��һ��...')
                adb.home(2, 1)
                time.sleep(3)
                lt = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
                name = adb.screencap(path=picturepath, module='Sleep', type=1)
                judge = os.path.exists(name)

                if judge == True:  # ���PC�����Ƿ������Ҫ�Աȵ�ͼ��
                    logO.info('====��ʼ����ͼ��ȶ�====')
                    result, coordinate = template_part(wifi_picture, name,num=0.64)

                    # ��ʼ����ͼ��ȶԣ�pass��ͼƬɾ����fail����
                    if result == False:
                        logO.info('Setting logo fail')
                        logO.info('Sleep pass')
                        time.sleep(1)
                        # ɾ��pass��ͼƬ
                        os.remove(name)
                    else:
                        logO.info('Setting logo fail')
                        logO.info('Sleep fail')
                        adb.order('input keyevent KEYCODE_POWER')
    except:
        adb.screencap(path=picturepath, type=1, module='Sleep_Error')

    adb.oneplus()
    time.sleep(5)

    try:
        name = adb.screencap(path=picturepath, module='Sleep', type=1)
        judge = os.path.exists(name)
        # ���PC�����Ƿ������Ҫ�Աȵ�ͼ��
        if judge == True:
            logO.info('====��ʼ����ͼ��ȶ�====')
            wifi_picture = picturepath + 'Setting.png'
            result, coordinate = template_part(wifi_picture, name,num=0.64)

            # ��ʼ����ͼ��ȶԣ�pass��ͼƬɾ����fail����
            if result == True:
                logO.info('Sleep logo pass')
                logO.info('Sleep up pass')
                time.sleep(1)
                # ɾ��pass��ͼƬ
                os.remove(name)
            else:
                logO.info('Sleep logo fail')
                logO.info('Sleep up fail')
                logO.info('�ٳ��Լ��һ��...')
                adb.home(2, 1)
                time.sleep(3)
                lt = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
                name = adb.screencap(path=picturepath, module='Sleep', type=1)
                judge = os.path.exists(name)

                if judge == True:  # ���PC�����Ƿ������Ҫ�Աȵ�ͼ��
                    logO.info('====��ʼ����ͼ��ȶ�====')
                    result, coordinate = template_part(wifi_picture, name,num=0.64)

                    # ��ʼ����ͼ��ȶԣ�pass��ͼƬɾ����fail����
                    if result == True:
                        logO.info('Sleep logo pass')
                        logO.info('Sleep up pass')
                        time.sleep(1)
                        # ɾ��pass��ͼƬ
                        os.remove(name)
                    else:
                        logO.info('Sleep logo fail')
                        logO.info('Sleep up fail')
                        adb.order('input keyevent KEYCODE_POWER')
    except:
        adb.screencap(path=picturepath, type=1, module='Sleep_Error')

    time.sleep(5)

    logO.info('��ִ�е�' + str(num) + '��')
