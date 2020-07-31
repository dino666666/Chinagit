#_*_encoding:GBK*_

import os
import time
import random
import logging
import threading
import queue

from lib.common.adbevent import adb
from lib.common.runinfo import run_log
from lib.common.logcat import log
from lib.common.part_image import template_part
from lib.common.initialize import initialize
from device_05.parameter import info

#ʵ����һ�����У�ʵ�����߳���������֮���ͨѶ
q = queue.Queue()
w = queue.Queue()
system_info = queue.Queue()

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
# ��ʼ��
initialize(device=device)
adb.app_stop(times=3,package='com.google.android.youtube.tv')

#���нű�ǰ�������ʷlogcat
adb.order('logcat -c')
logO.info('logcat -c')

def thread1():
    #�ж��Ƿ���Ҫ�˳��ű�ִ��
    while True:
        end = input('������q��������:')
        if end == 'q':
            q.put('q')
            break

def thread2():
    loginfo = adb.order('logcat')
    read = loginfo.readline()

    while read:

        if not q.empty():
            if q.get() == 'q':
                time.sleep(2)
                q.put('q')
                break

        if not system_info.empty():
            logO.info(system_info.get())
            logO.info(read)
            system_info.queue.clear()

        if not w.empty():
            result,win = adb.windows('youtube')
            if result == False:
                logO.info(read)
                logO.info('��ʼ�����쳣����...')
                initialize(device=device)
                adb.app_stop(times=3, package='com.google.android.youtube.tv')
                # ����YouTube
                result, win = adb.app_start(times=35, keyword='youtube',
                                            package='com.google.android.youtube.tv')
                # �ж�YouTube�Ƿ������ɹ�
                if result == True:
                    logO.info('YouTube started successfully')
                else:
                    logO.info('YouTube startup failed')
                    logO.info('����ʧ�ܣ������쳣��������...')

                adb.ok(1,5)
            w.queue.clear()
        read = loginfo.readline()

def thread3():
    a = os.popen('adb -s ' + device + ' shell top -d 5')
    read = a.readline()
    number = 0

    while read:
        # print(read)
        if not q.empty():
            if q.get() == 'q':
                time.sleep(2)
                q.put('q')
                break

        info = read.split(' ')
        mem = 0
        mem_list = []
        for i in info:
            # print(i)
            if '%cpu' in i:
                total_cpu = i.split('%')[0]
                # print(i)
                # print(total_cpu)

            if 'idle' in i:
                # print(i)
                idle_cpu = i.split('%')[0]
                # print(idle_cpu)

                try:
                    use = int(total_cpu) - int(idle_cpu)
                    logO.info('��ǰCPUʹ����:' + str(use) + '%')
                    if use > 390:
                        system_info.put('CPU')
                        print('cpu')
                        number += 1
                except:
                    pass

            if 'Mem' in i:
                # print(read)
                # print(info)
                mem = 1

            if mem == 1:
                if 'k' in i:
                    # print(i)
                    mem_list.append(i.split('k')[0])
                    # print(mem_list)
                    try:
                        buffers_mem = (int(mem_list[3]) / int(mem_list[0])) * 100
                        use_men = (int(mem_list[1]) / int(mem_list[0])) * 100
                        logO.info('��ǰ�ڴ�ʹ����' + str(use_men) + "%")
                        logO.info('��ǰ�����ڴ�ռ�ݣ�' + str(buffers_mem) + '%')
                        if use_men > 99:
                            system_info.put('Mem')
                            print('mem')
                            number += 1

                        if use_men < 0.1:
                            system_info.put('buffers')
                            print('buff')
                            number += 1
                    except:
                        pass

        if number >= 1:
            logO.info(read)
            if number > 60:
                ps = adb.order('ps -ef').read()
                logO.info(ps)
                number = 0

        read = a.readline()

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

#��logcat��ģ������ΪPlaybackControl
log.open('PlaybackControl')

# ����YouTube
result, win = adb.app_start(times=35, keyword='youtube',
                            package='com.google.android.youtube.tv')
# �ж�YouTube�Ƿ������ɹ�
if result == True:
    logO.info('YouTube started successfully')
else:
    logO.info('YouTube startup failed')

#ѡ��Video
adb.ok(1,40)
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
    adb.up(2,2)

    # ��ͼ����ȡ����������,�����������
    for i in range(3):
        template_name = picturepath + 'YouTube_bar.png'
        picture_name = adb.screencap(path=picturepath, module='YouTube', type=1)
        judge = os.path.exists(picture_name)

        # �жϽ�ͼ�Ƿ����
        if judge == True:
            try:
                result = False
                result,coordinate_value1 = template_part(picture1=template_name,picture2=picture_name,type = 1)
                logO.info('coordinate_value1[0]��' + str(coordinate_value1[0]))
                logO.info('coordinate_value1[temp]��' + str(coordinate_value1[1]))
            except:
                w.put('p')
                time.sleep(60)
            finally:
                #�ҵ����������ж��н�����Ƶ����
                if result == True:
                    logO.info('���ڽ�����...')
                else:
                    logO.info('�Ҳ���������...')


            template_name = picturepath + 'YouTube_play.png'
            try:
                result = False
                result, coordinate_value = template_part(picture1=template_name, picture2=picture_name)
            except:
                w.put('p')
                time.sleep(60)
            finally:
                 # �ж���Ƶ���ڲ��Ż�������ͣ
                if result == True:
                    logO.info('��ǰ����״̬Ϊ��Play')
                else:
                    logO.info('��ǰ���ſ��ܴ�����ͣ')
                    adb.ok(1,2)

                time.sleep(60)
            # ��������������ֵ
            adb.up(2,2)
            template_name = picturepath + 'YouTube_bar.png'
            picture_name = adb.screencap(path=picturepath, module='YouTube', type=1)
            judge = os.path.exists(picture_name)

            # �жϽ�ͼ�Ƿ����
            if judge == True:
                try:
                    result = False
                    difference_value = 0
                    result, coordinate_value2 = template_part(picture1=template_name, picture2=picture_name, type=1)
                    logO.info('coordinate_value2[0]��' + str(coordinate_value2[0]))
                    logO.info('coordinate_value2[temp]��' + str(coordinate_value2[1]))
                    difference_value = int(coordinate_value2[0]) - int(coordinate_value1[0])
                except:
                    w.put('p')
                finally:
                    # �ҵ����������ж��н�����Ƶ����
                    if result == True:
                        logO.info('���ڽ�����...')
                    else:
                        logO.info('�Ҳ���������...')

                    logO.info('difference_value�����ţ�:' + str(difference_value))

                    if difference_value > 10:
                        logO.info('�����������߶�,��Ƶ���ڲ���...')
                    else:
                        logO.info('������û�����߶�,��Ƶ����û�ڲ���')
                        w.put('p')
                        time.sleep(60)

            print('break')
            break

        else:
            w.put('p')
            time.sleep(60)

    adb.ok(2,2)

    # ��ͼ����ȡ����������,��鲥��
    for i in range(3):
        template_name = picturepath + 'YouTube_pause.png'
        picture_name = adb.screencap(path=picturepath, module='YouTube', type=1)
        judge = os.path.exists(picture_name)

        # �жϽ�ͼ�Ƿ����
        if judge == True:
            try:
                result = False
                result, coordinate_value1 = template_part(picture1=template_name, picture2=picture_name)
            except:
                w.put('p')
                time.sleep(60)
            finally:
                # ����ͼ���ж���Ƶ�Ƿ�����ͣ
                if result == True:
                    logO.info('��Ƶ����ͣ...')
                else:
                    logO.info('��Ƶδ��ͣ...')

            adb.up(1,2)
            template_name = picturepath + 'YouTube_bar.png'
            picture_name = adb.screencap(path=picturepath, module='YouTube', type=1)
            judge = os.path.exists(picture_name)

            # �жϽ�ͼ�Ƿ����
            if judge == True:
                try:
                    result, coordinate_value1 = template_part(picture1=template_name, picture2=picture_name)
                    logO.info('coordinate_value1[0]��' + str(coordinate_value1[0]))
                    logO.info('coordinate_value1[temp]��' + str(coordinate_value1[1]))
                except:
                    w.put('p')
                    time.sleep(60)
                finally:
                    if result == True:
                        logO.info('���ڽ�����...')
                    else:
                        logO.info('�Ҳ���������...')

            adb.left(8,1,type=1)

            template_name = picturepath + 'YouTube_bar.png'
            picture_name = adb.screencap(path=picturepath, module='YouTube', type=1)
            judge = os.path.exists(picture_name)

            # �жϽ�ͼ�Ƿ����
            if judge == True:
                try:
                    result = False
                    result, coordinate_value = template_part(picture1=template_name, picture2=picture_name)
                    logO.info('coordinate_value[0]��' + str(coordinate_value[0]))
                    logO.info('coordinate_value[temp]��' + str(coordinate_value[1]))
                except:
                    w.put('p')
                    time.sleep(60)
                finally:
                    if result == True:
                        logO.info('�������ƶ��ɹ�...')
                    else:
                        logO.info('�������ƶ�ʧ��...')

            # ������Ƶ
            adb.ok(1,10)
            adb.up(2,2)
            template_name = picturepath + 'YouTube_bar.png'
            picture_name = adb.screencap(path=picturepath, module='YouTube', type=1)
            judge = os.path.exists(picture_name)

            # �жϽ�ͼ�Ƿ����
            if judge == True:
                try:
                    result = False
                    difference_value = 0
                    result, coordinate_value2 = template_part(picture1=template_name, picture2=picture_name)
                    logO.info('coordinate_value[0]��' + str(coordinate_value2[0]))
                    logO.info('coordinate_value[temp]��' + str(coordinate_value2[1]))
                    difference_value = int(coordinate_value2[0]) - int(coordinate_value1[0])
                except:
                    w.put('p')
                    time.sleep(60)
                finally:
                    if result == True:
                        logO.info('���ڽ�����...')
                    else:
                        logO.info('�Ҳ���������...')


            logO.info('difference_value�����ˣ�:' + str(difference_value))

            if difference_value < -10:
                logO.info('���˳ɹ�...')
            else:
                logO.info('����ʧ��...')
                w.put('p')
                time.sleep(60)

            adb.up(2, 2)
            adb.right(3,1,type=1)
            template_name = picturepath + 'YouTube_bar.png'
            picture_name = adb.screencap(path=picturepath, module='YouTube', type=1)
            judge = os.path.exists(picture_name)

            if judge == True:
                try:
                    result, coordinate_value = template_part(picture1=template_name, picture2=picture_name, type=1)
                    logO.info('coordinate_value[0]��' + str(coordinate_value[0]))
                    logO.info('coordinate_value[temp]��' + str(coordinate_value[1]))
                except:
                    w.put('p')
                    time.sleep(60)
                finally:
                    # �ҵ����������ж��н�����Ƶ����
                    if result == True:
                        logO.info('���ڽ�����...')
                    else:
                        logO.info('�Ҳ���������...')

            adb.ok(1,3)
            adb.up(2,2)
            template_name = picturepath + 'YouTube_bar.png'
            picture_name = adb.screencap(path=picturepath, module='YouTube', type=1)
            judge = os.path.exists(picture_name)

            if judge == True:
                try:
                    result = False
                    difference_value = 0
                    result, coordinate_value3 = template_part(picture1=template_name, picture2=picture_name, type=1)
                    logO.info('coordinate_value3[0]��' + str(coordinate_value3[0]))
                    logO.info('coordinate_value3[temp]��' + str(coordinate_value3[1]))
                    difference_value = int(coordinate_value3[0]) - int(coordinate_value2[0])
                except:
                    w.put('p')
                    time.sleep(60)
                finally:
                    # �ҵ����������ж��н�����Ƶ����
                    if result == True:
                        logO.info('���ڽ�����...')
                    else:
                        logO.info('�Ҳ���������...')

                logO.info('difference_value�������:' + str(difference_value))

                if difference_value > 10:
                    logO.info('����ɹ�...')
                else:
                    logO.info('���ʧ��...')

            print('break')
            break

        else:
            w.put('p')
            time.sleep(60)

    if num %3 == 0:
        adb.down(2,2)
    else:
        pass

    adb.ok(1,25)

    time.sleep(10)
    logO.info('break')

    logO.info('��ִ�����'+str(num)+'��')