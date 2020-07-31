#_*_encoding:GBK*_

def YouTube_run(count):
    import os
    import time
    import logging
    import threading
    import queue
    import cv2,time,logging,os
    import numpy as np
    # ��
    from lib.common.adbevent import adb
    from lib.common.runinfo import run_log
    from lib.common.logcat import log
    from lib.common.BasePage import Basepage
    from lib.common.part_image import template_part
    from skimage.measure import compare_ssim
    from lib.common.runinfo import run_log
    from lib.tools.csv_write import csv_write
    from appium.webdriver.common.mobileby import MobileBy
    # ����
    from lib.common.initialize import initialize
    from lib.common.template_matching import compare
    from device_03.parameter import info


    logging.basicConfig(level=logging.DEBUG,format=' %(asctime)s - %(levelname)s - %(message)s')
    logging.disable(logging.DEBUG)
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
    csv_w = csv_write(path=picturepath + 'Youtube.csv')
    #�ű�������Ϣ
    logging.basicConfig(level=logging.DEBUG,format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

    csv_w.open()
    csv_w.write(['num','time'])
    time.sleep(1)
    csv_w.close()
    num = 1
    video_num = 0
    while True:
        if num > count:
            break

        # д��������Ϣ
        logO.info('��ʼִ�е�' + str(num) + '��')
        flag = 0
        adb.oneplus(type=1)
        T0 = time.time()
        adb.left(2)
        result, window = adb.windows('ActionsDialog')
        if result == True:
            adb.ok()
        else:
            adb.order('input keyevent KEYCODE_POWER')
        time.sleep(10)
        # ÿ��0.3S���һ�ε�ǰ�Ӵ����ж�TV�Ƿ��Ѿ��������
        for qc in range(180):
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

        adb.screencap(path=picturepath, type=1, module='WiFi_routine_' + str(num) + '_')
        time.sleep(3)

        # �ж��������Ƿ���Google Lanucher
        result, window = adb.windows('com.google.android.tvlauncher')
        logO.info(window)

        if result == True:
            logO.info('��ǰ���洦��Google Lanucher')
        else:
            logO.info('��ǰ���治����Google Lanucher')
            adb.screencap(path=picturepath, type=1, module='AC_' + str(num) + '_')
        time.sleep(10)
        # ��logcat
        log.open('YouTube')

        APP_start = 0
        APP_wait = 0
        camera = cv2.VideoCapture(0)
        # ��������ͷͼ��
        es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
        #getStructuringElement��������ȡ�ṹ��Ԫ��
        #��̬ѧ����
        #��Բ�Σ�MORPH_ELLIPSE;
        kernel = np.ones((5, 5), np.uint8)
        #��numpy�������Լ���Ҫ�Ľṹ��Ԫ��
        background = None
        number=0
        video_number=1
        path='/home/oneplus/Python-Video/'
        ## some videowriter props
        sz = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
              int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        # ��ȡ֡�ĳߴ�
        # CAP_PROP_FRAME_WIDTH,֡�Ŀ��
        # CAP_PROP_FRAME_HEIGHT,֡�ĸ߶�
        fps = int(camera.get(cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc(*'mpeg')
        # ��ʽ
        ## open and set props
        vout = cv2.VideoWriter()
        vt = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '-' + str(video_number)
        video_name = '/home/oneplus/Python-Video/Video-' + str(vt) + '.mp4'
        vout.open(video_name, fourcc, fps, sz, True)
        video_number += 1
        print('video number:', video_number)
        ret, frame = camera.read()
        time.sleep(5)
        adb.youtube()
        T0 = time.time()
        while True:
            ret, frame = camera.read()

            if background is None:
                background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                background = cv2.GaussianBlur(background, (21, 21), 0)
                continue

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # ת����ɫ�ռ�,�Ҷ�ͼ
            # cv2.imshow('hui',gray_frame)
            gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)
            # cv2.imshow('goasi', gray_frame)
            #��˹ģ��
            diff = cv2.absdiff(background, gray_frame)
            (score, no) = compare_ssim(background, gray_frame, full=True)
            # logO.info(score)
            if float(score) <=0.8 and APP_start <= 2:
                APP_start += 1
                print('APP_start1:',APP_start)
                logO.info(score)
                if APP_start >= 2:
                    APP_start = 20

            if APP_start >= 20 and float(score)>= 0.95:
                logO.info(score)
                APP_start += 1
                print('APP_start2:',APP_start)
                if APP_start >= 50:
                    APP_wait = 1
                    APP_start = 10
            if APP_start == 10:
                logO.info(score)
            if APP_wait == 1 and float(score) <= 0.9:
                logO.info(score)
                T1 = time.time()
                print('APP_wait:',APP_wait)
                logO.info('APP start suceess')
                cv2.destroyAllWindows()
                print('cv2.destroyAllWindows()')
                vout.release()
                print('vout.release()')
                camera.release()
                print('camera.release()')
                break
            if APP_start == 10 and float(score)>= 0.95:
                if time.time() - T0 >= 60:
                    logO.info('APP start suceess')
                    cv2.destroyAllWindows()
                    print('cv2.destroyAllWindows()')
                    vout.release()
                    print('vout.release()')
                    camera.release()
                    print('camera.release()')
                    continue
            # #��ò��ͼ������ͼƬ�Ĳ���
            # diff = cv2.threshold(diff, 5, 255, cv2.THRESH_BINARY)[temp]
            # # һ����ɫ��ͼƬ�����Ҫô�ǰ�ɫҪô���Ǻ�ɫ��255Ϊ��ɫ��0Ϊ��ɫ������5��ֵ���Ϊ255����ɫ��ͼ���ֵ��
            # # cv2.imshow('gray_frame',gray_frame)
            # diff = cv2.dilate(diff, es, iterations=2)
            # # ���ͣ�������ͼƬ�߽粻һ���ĵط�����
            # cnts, hierarchy = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # #Ѱ�Ҳ�ͬ�����ͺ������
            # # cv2.RETR_EXTERNALֻ���������
            # #cv2.CHAIN_APPROX_SIMPLE�൱����һ�����ΰ����ͺ�Ĳ�ͬ���������������
            # # logO.info(cnts)
            video_num += 1
            if video_num % 2 == 0:
                background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                background = cv2.GaussianBlur(background, (21, 21), 0)
            #
            # cv2.putText(frame, str(number), (10, 20), cv2.FONT_HERSHEY_PLAIN, temp, (0, 255, 0), temp, cv2.LINE_AA)
            cv2.imshow('Video', frame)
            # cv2.imshow('dif', diff)

            if cv2.waitKey(int(1000 / 12)) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
        camera.release()
        li = []
        T = (T1 - T0)*1000
        logO.info('YouTube Start time:' + str(T) + 'ms')
        li.append(str(num))
        li.append(str(T))
        print(li)
        logO.info(li)
        csv_w.open(type=1)
        csv_w.write(li)
        time.sleep(1)
        csv_w.close()
        num += 1
if __name__=="__main__":
    YouTube_run(30)