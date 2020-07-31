#_*_encoding:GBK*_
# �����豸����Ҫ���ź�ԴѡΪHDMI1
# һ������ʮ��APP��Live TV��Google Movies��Hotstart��Zee5��JioCinema��Hungama��FileBrowser��Prime video��YouTube��Netflix
# ����ʱ��Ҫ������˻���¼
# APP�������η�����APP��Live TV��Google Movies��Hotstart��Zee5��JioCinema��Hungama��FileBrowser��voot��shemarooMe��MXPlayer TV
import time
import random
import logging
import threading
import queue

from lib.common.adbevent import adb
from lib.common.runinfo import run_log
from lib.common.logcat import log
from lib.common.initialize import initialize
print('(temp)һ�������˸�APP��Google Movies��Hotstart��Zee5��JioCinema��Hungama��voot��shemarooMe��MXPlayer TV')
print('(2)����ʱ��Ҫ������˻���¼')
print('(3)APP�������η�����APP��Live TV��Google Movies��Hotstart��Zee5��JioCinema��Hungama��FileBrowser��voot��shemarooMe��MXPlayer TV')
#��ʼ���豸��Ϣ�Լ��ű����й����в������ļ�����·��
device = '011000AL370013B4D6'
path = 'C:\\Users\\huanglei\\Downloads\\task\\'

#ʵ����һ�����У�ʵ�����߳���������֮���ͨѶ
q=queue.Queue()

def thread():
    #�ж��Ƿ���Ҫ�˳��ű�ִ��
    while True:
        end = input('������q��������:')
        if end == 'q':
            q.put('q')
            break

#����ű����й����в������ļ�·��
logpath = path 
picturepath = path
runpath = path
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

# ��ʼ���豸
initialize(device=device)

#���нű�ǰ�������ʷlogcat
adb.order('logcat -c')
logO.info('logcat -c')

#��ʼ���߳�
thread_thred = threading.Thread(target=thread)
#���߳�
thread_thred.start()

#����һ�����֣�����ѭ������
num=0

# ץȡlog
log.open(module='App_Start')

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

    logO.info('========����Google Movies========')
    for i in range(3):
        # ����Google Movies����
        adb.home(2, 0.5)
        adb.right(1)
        adb.back(1,0.5)
        adb.right(1,2)
        adb.ok(1,20)
        # �ж�Google Movies�Ƿ������ɹ�
        result, window =adb.windows('movies')
        if result == True:
            logO.info('Google Movies started successfully')
            break
        else:
            logO.info('Google Movies startup failed')

    if 'WatchActivity' in window:
        pass
    elif 'details' in window:
        adb.ok()
    else:
        adb.down(1,1)
        adb.right(1, 1)
        adb.ok(2, 3)
    time.sleep(30)

    logO.info('========����Netflix========')
    for i in range(3):
        # ����Netflix����
        adb.netflix()
        time.sleep(20)
        # �ж�Netflix�Ƿ������ɹ�
        result, window = adb.windows('netflix')
        if result == True:
            logO.info('Netflix started successfully')
            break
        else:
            logO.info('Neflix startup failed')
    adb.up(2, 1)
    adb.ok(2)
    time.sleep(30)
    adb.home(1,2)


    logO.info('========����HotStart========')
    # ����HotStart����
    adb.right(1, 2)
    adb.ok(1, 25)
    for i in range(3):
        # �ж�HotStart�Ƿ������ɹ�
        result, window = adb.windows('hotstar')
        if result == True:
            logO.info('HotStart started successfully')
            break
        else:
            logO.info('HotStart startup failed')
            adb.home(2, 0.5)
            adb.right(3)
            adb.back(1, 0.5)
            adb.right(2, 1)
            adb.ok(1, 20)
    for i in range(3):
        result, window = adb.windows('player')
        if result == True:
            break
        else:
            adb.ok(1,2)
    time.sleep(30)
    adb.home(1,2)

    logO.info('========����ZEE5========')
    # ����ZEE5����
    adb.right(1, 2)
    adb.ok(1, 25)
    for i in range(3):
        # �ж�ZEE5�Ƿ������ɹ�
        result, window = adb.windows('graymatrix')
        if result == True:
            logO.info('ZEE5 started successfully')
            break
        else:
            logO.info('ZEE5 startup failed')
            adb.home(2, 0.5)
            adb.right(3)
            adb.back(1, 0.5)
            adb.right(3, 1)
            adb.ok(1, 25)
    if 'PlaybackOverlayActivity' in window:
        pass
    else:
        adb.back(3)
        adb.left(3)
        adb.right(2,1)
        adb.ok(1,1)
        adb.down(2,1)
        adb.ok(4, 3)
    time.sleep(30)
    adb.home(1,2)

    logO.info('========����JioCinema========')
    # ����JioCinema����
    adb.right(1, 2)
    adb.ok(1, 25)
    for i in range(3):
        # �ж�JioCinema�Ƿ������ɹ�
        result, window = adb.windows('jio.media')
        if result == True:
            logO.info('JioCinema started successfully')
            break
        else:
            logO.info('JioCinema startup failed')
            adb.home(2, 0.5)
            adb.right(1)
            adb.back(1, 0.5)
            adb.right(4, 1)
            adb.ok(1, 20)
    if 'player' in window:
        pass
    else:
        adb.down(1, 2)
        adb.ok(4, 5)
    time.sleep(30)
    adb.home(1,2)

    logO.info('========����Hungama========')
    # ����Hungama
    adb.right(1, 2)
    adb.ok(1, 25)
    for i in range(3):
        # �ж�Hungama�Ƿ������ɹ�
        result, window = adb.windows('hungama')
        if result == True:
            logO.info('Hungama started successfully')
            break
        else:
            logO.info('Hungama startup failed')
            adb.home(2, 0.5)
            adb.right(1)
            adb.back(1, 0.5)
            adb.right(5, 1)
            adb.ok(1, 20)
    if 'PlayVideoActivity' in window:
        pass
    elif 'DetailActivity' in window:
        adb.left(2)
        adb.ok()
    else:
        adb.right(2, 1)
        adb.down(1,1)
        adb.ok(1, 5)
    time.sleep(30)

    logO.info('========����prime video========')
    for i in range(3):
        # ����prime video
        adb.prime()
        time.sleep(25)
        # �ж�prime video�Ƿ������ɹ�
        result, window = adb.windows('amazon')
        if result == True:
            logO.info('prime video started successfully')
            break
        else:
            logO.info('prime video startup failed')

    adb.down(1, 2)
    adb.ok(1, 5)
    adb.down(3,1)
    adb.left(3,1)
    adb.ok(1,5)
    time.sleep(30)

    logO.info('========����YouTube========')
    for i in range(3):
        # ����YouTube����
        adb.youtube()
        time.sleep(20)
        # �ж�YouTube�Ƿ������ɹ�
        result, window = adb.windows('youtube')
        if result == True:
            logO.info('YouTube started successfully')
            break
        else:
            logO.info('YouTube startup failed')
    adb.down(2)
    adb.ok()
    time.sleep(30)
    adb.home(1,2)

    # ����voot����
    adb.right(3, 1)
    adb.ok(1, 25)
    logO.info('========����voot========')
    for i in range(3):
        # �ж�voot�Ƿ������ɹ�
        result, window = adb.windows('voot')
        if result == True:
            logO.info('voot started successfully')
            break
        else:
            logO.info('voot startup failed')
            adb.home(2, 0.5)
            adb.right(1)
            adb.back(1, 0.5)
            adb.right(8, 1)
            adb.ok(1, 25)
    for i in range(3):
        result, window = adb.windows('player')
        if result == True:
            break
        else:
            adb.right(1,2)
            adb.ok(1,2)
    time.sleep(30)
    adb.home(1,2)

    # ����ShemarooMe����
    adb.right(1, 1)
    adb.ok(1, 25)
    logO.info('========����ShemarooMe========')
    for i in range(3):
        # �ж�ShemarooMe�Ƿ������ɹ�
        result, window = adb.windows('shemaroome')
        if result == True:
            logO.info('ShemarooMe started successfully')
            break
        else:
            logO.info('ShemarooMe startup failed')
            adb.home(2, 0.5)
            adb.right(1)
            adb.back(1, 0.5)
            adb.right(9, 1)
            adb.ok(1, 25)
    for i in range(3):
        result, window = adb.windows('ExoVideoPlayer')
        if result == True:
            break
        else:
            adb.right(1, 2)
            adb.ok(1, 2)
    time.sleep(30)
    adb.home(1,2)

    # ����MXPLAYER TV����
    adb.right(1, 1)
    adb.ok(1, 25)
    logO.info('========����MXPLAYER TV========')
    for i in range(3):
        # �ж�MXPLAYER TV�Ƿ������ɹ�
        result, window = adb.windows('mxtech')
        if result == True:
            logO.info('MXPLAYER TV started successfully')
            break
        else:
            logO.info('MXPLAYER TV startup failed')
            adb.home(2, 0.5)
            adb.right(1)
            adb.back(1, 0.5)
            adb.right(10, 1)
            adb.ok(1, 25)
    for i in range(3):
        result, window = adb.windows('newplay')
        if result == True:
            break
        else:
            logO.info('voot startup failed')
            adb.down(1, 2)
            adb.ok(1, 2)
    time.sleep(30)
    adb.home(1,2)

    logO.info('��ִ����' + str(num) + '��')