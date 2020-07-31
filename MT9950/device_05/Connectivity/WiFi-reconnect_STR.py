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

# ��ʼ��
initialize(device=device)
#����webdriver����
driver.Open()
#���wifi�����Ƿ�ΪON,ΪOFFʱ���
text = driver.find_element(MobileBy.XPATH,
                         '//android.support.v7.widget.RecyclerView/android.widget.LinearLayout[temp]/android.widget.LinearLayout[2]/android.widget.Switch').text
if text == 'OFF':
    driver.find_element(MobileBy.XPATH,"//*[@text='Wi-Fi']").click()
else:
    pass

time.sleep(3)

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
        log.open('sleep')
        # ÿ��ѭ��num+temp
        num += 1
        # д��������Ϣ
        logO.info('��ʼִ�е�' + str(num) + '��')
        adb.oneplus(type=1)
        result, window = adb.windows('ActionsDialog')
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
                result, coordinate = template_part(wifi_picture, name, num=0.64)

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
                        result, coordinate = template_part(wifi_picture, name, num=0.64)

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

        name = adb.screencap(path=picturepath, module='WiFi', type=1)
        judge = os.path.exists(name)
        # ���PC�����Ƿ������Ҫ�Աȵ�ͼ��
        if judge == True:
            logO.info('====��ʼ����ͼ��ȶ�====')
            wifi_picture = picturepath + 'WiFi_ON.png'
            result, coordinate = template_part(wifi_picture, name)

            # ��ʼ����ͼ��ȶԣ�pass��ͼƬɾ����fail����
            if result == True:
                logO.info('WI-FIͼ����ʾΪconnected...')
                logO.info('pass')
                logO.info('wake up success')
                time.sleep(1)
                # ɾ��pass��ͼƬ
                # os.remove(name)
            else:
                logO.info('WI-FIͼ����ʾΪdisconnect...')
                logO.info('fail')
                logO.info('wake-up failure')
                logO.info('�ٳ��Լ��һ��...')
                adb.oneplus()
                time.sleep(3)
                adb.back(2)
                adb.home()
                time.sleep(5)
                lt = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
                name = adb.screencap(path=picturepath, module='WiFi', type=1)
                judge = os.path.exists(name)

                if judge == True:  # ���PC�����Ƿ������Ҫ�Աȵ�ͼ��
                    logO.info('====��ʼ����ͼ��ȶ�====')
                    result, coordinate = template_part(wifi_picture, name)

                    # ��ʼ����ͼ��ȶԣ�pass��ͼƬɾ����fail����
                    if result == True:
                        logO.info('WI-FIͼ����ʾΪconnected...')
                        logO.info('pass')
                        time.sleep(1)
                        # ɾ��pass��ͼƬ
                        os.remove(name)
                    else:
                        logO.info('WI-FIͼ����ʾΪdisconnect...')
                        logO.info('wake-up failure')
                        adb.oneplus()
                        time.sleep(3)
                        adb.back(2)
                        adb.home()
                        logO.info('fail')
    except:
        logO.info('error')
        adb.screencap(path=picturepath, type=1, module='WiFi_Error')

    for i in range(3):

        result,window = adb.app_start(times=3,keyword='NetworkActivity',package='com.android.tv.settings/com.android.tv.settings.connectivity.NetworkActivity')
        if result == True:
            logO.info('WiFi started successfully')
            break
        else:
            logO.info('WiFi startup failed')
            adb.screencap(type=1,module='mode')

    wifi_flag = 0
    # ����3��ȥ����webdriver
    for i in range(5):
        try:
            driver.Open()
            time.sleep(5)
            #���wifi����״̬
            if driver.find(MobileBy.XPATH,"//*[contains(@text,'Connect')]")==True:
                wifi_flag = 1
                driver.Quit()
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
                driver.Quit()
                break
        except:
            try:
                pass
            except:
                pass

    if wifi_flag == 0:
        logO.info('WI-FI����ʧ��...')
        adb.screencap(path=picturepath, type=1, module='WiFi_RC')
    else:
        logO.info('WI-FI�����ɹ�...')

    adb.back(3,1)



    ping = adb.order('"ping -c 10 www.google.com"')
    read = ping.readline()

    while read:
        logO.info(read)
        drop = read.split(' ')

        for probability in drop:
            if '%' in probability:
                logO.info('������:'+probability)

        read = ping.readline()
    log.close()
    logO.info('��ִ�е�' + str(num) + '��')