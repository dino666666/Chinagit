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
from lib.common.BasePage import Basepage
from lib.common.part_image import template_part
from appium.webdriver.common.mobileby import MobileBy
# ����
from lib.common.initialize import initialize
from lib.common.template_matching import compare
from device_01.parameter import info

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
#WIFI
driver=Basepage(device=device,driver='driver',appPackage='com.android.tv.settings',
                appActivity='connectivity.NetworkActivity',port=8200,url='http://127.0.0.1:4723/wd/hub')

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

while True:
    #ʹ���쳣�������̣���ֹ�Ҳ���Ԫ�ر���
    try:

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
        result, window = adb.windows('ActionsDialog')
        if result == True:
            pass
        else:
            adb.order('input keyevent --longpress KEYCODE_POWER')

        adb.right(3,1)
        adb.ok()
        time.sleep(10)

        # ÿ��0.3S���һ�ε�ǰ�Ӵ����ж�TV�Ƿ��Ѿ��������
        for i in range(1000):
            time.sleep(0.3)
            result, window = adb.windows('com.google.android.tvlauncher')

            if result == True:
                flag = 1
                logO.info(window)
                time.sleep(3)
                break

        time.sleep(3)
        # �ж��������Ƿ���Google Lanucher
        result, window = adb.windows('com.google.android.tvlauncher')
        logO.info(window)

        if result == True:
            logO.info('��ǰ���洦��Google Lanucher')
        else:
            logO.info('��ǰ���治����Google Lanucher')

        # ��logcat��WiFi_reconnect
        log.open('WiFi_reconnect')
        time.sleep(3)

        wifi_flag = 0
        # ����3��ȥ����webdriver
        for i in range(5):
            try:
                driver.Open()
                time.sleep(3)
                #���wifi����״̬
                if driver.find(MobileBy.XPATH,"//*[contains(@text,'Connect')]")==True:
                    wifi_flag = 1
                    break
                else:
                    wifi_flag = 0
                    # ���wifi�����Ƿ�ΪON,ΪOFFʱ���
                    text = driver.find_element(MobileBy.XPATH,
                                               '//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[temp]/android.widget.LinearLayout[2]/android.widget.Switch').text
                    if text == 'OFF':
                        adb.screencap(path=picturepath, type=1, module='WiFi_Error')
                        logO.info('wifib switch is off')
                        driver.find_element(MobileBy.XPATH, "//*[@text='Wi-Fi']").click()
                    else:
                        pass

                    time.sleep(3)
                    break
            except:
                try:
                    driver.Quit()
                except:
                    pass

        if wifi_flag == 0:
            logO.info('WI-FI����ʧ��...')
            adb.screencap(path=picturepath, type=1, module='WiFi_RC')
        else:
            logO.info('WI-FI�����ɹ�...')

        adb.back(3,1)
        adb.home()
        driver.Quit()
        name = adb.screencap(path=picturepath,module='WiFi',type=1)
        judge = os.path.exists(name)

        # ���PC�����Ƿ������Ҫ�Աȵ�ͼ��
        if judge == True:
            logO.info('====��ʼ����ͼ��ȶ�====')
            wifi_picture = picturepath+'WiFi_ON.png'
            result, coordinate = template_part(wifi_picture,name)

            # ��ʼ����ͼ��ȶԣ�pass��ͼƬɾ����fail����
            if result == True:
                logO.info('WI-FIͼ����ʾΪconnected...')
                logO.info('pass')
                time.sleep(1)
                # ɾ��pass��ͼƬ
                os.remove(name)
            else:
                logO.info('WI-FIͼ����ʾΪdisconnect...')
                logO.info('fail')
                logO.info('�ٳ��Լ��һ��...')
                adb.home(2,1)
                time.sleep(3)
                lt = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
                name = adb.screencap(path=picturepath,module='WiFi',type=1)
                judge = os.path.exists(name)

                if judge == True:  # ���PC�����Ƿ������Ҫ�Աȵ�ͼ��
                    logO.info('====��ʼ����ͼ��ȶ�====')
                    result, coordinate = template_part(wifi_picture,name)

                    # ��ʼ����ͼ��ȶԣ�pass��ͼƬɾ����fail����
                    if result == True:
                        logO.info('WI-FIͼ����ʾΪconnected...')
                        logO.info('pass')
                        time.sleep(1)
                        # ɾ��pass��ͼƬ
                        os.remove(name)
                    else:
                        logO.info('WI-FIͼ����ʾΪdisconnect...')
                        logO.info('fail')
    except:
        logO.info('error')
        adb.screencap(path=picturepath, type=1, module='WiFi_Error')
    ping = adb.order('"ping -c 10 www.google.com"')
    read = ping.readline()

    while read:
        logO.info(read)
        drop = read.split(' ')

        for probability in drop:
            if '%' in probability:
                logO.info('������:'+probability)

        read = ping.readline()

    logO.info('��ִ�е�' + str(num) + '��')
