#_*_encoding:GBK*_
# 运行设备是需要将信号源选为HDMI1
# 一共启动十个APP：Live TV、Google Movies、Hotstart、Zee5、JioCinema、Hungama、FileBrowser、Prime video、YouTube、Netflix
# 测试时需要将相关账户登录
# APP栏上依次放以下APP：Live TV、Google Movies、Hotstart、Zee5、JioCinema、Hungama、FileBrowser、voot、shemarooMe、MXPlayer TV
import time
import random
import logging
import threading
import queue

from lib.common.adbevent import adb
from lib.common.runinfo import run_log
from lib.common.logcat import log
from lib.common.initialize import initialize
print('(temp)一共启动八个APP：Google Movies、Hotstart、Zee5、JioCinema、Hungama、voot、shemarooMe、MXPlayer TV')
print('(2)测试时需要将相关账户登录')
print('(3)APP栏上依次放以下APP：Live TV、Google Movies、Hotstart、Zee5、JioCinema、Hungama、FileBrowser、voot、shemarooMe、MXPlayer TV')
#初始化设备信息以及脚本运行过程中产生的文件保存路径
device = '011000AL370013B4D6'
path = 'C:\\Users\\huanglei\\Downloads\\task\\'

#实例化一个队列，实现子线程与主进程之间的通讯
q=queue.Queue()

def thread():
    #判断是否需要退出脚本执行
    while True:
        end = input('请输入q结束程序:')
        if end == 'q':
            q.put('q')
            break

#定义脚本运行过程中产生的文件路径
logpath = path 
picturepath = path
runpath = path
#实例化
#运行信息
logO = run_log(logging_path=runpath,logger=device).getlog()
#设备信息
adb = adb(device=device)
#logcat信息
log = log(log_path=logpath,device=device)

#脚本调试信息
logging.basicConfig(level=logging.DEBUG,format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

#script execution
logO.info('script execution')
time.sleep(2)

# 初始化设备
initialize(device=device)

#运行脚本前，清除历史logcat
adb.order('logcat -c')
logO.info('logcat -c')

#初始化线程
thread_thred = threading.Thread(target=thread)
#打开线程
thread_thred.start()

#定义一个数字，用作循环计数
num=0

# 抓取log
log.open(module='App_Start')

while True:
    flag = 0
    # 判断是否需要跳出循环，结束运行中的脚本
    if not q.empty():
        if q.get() == 'q':
            # 结束运行脚本时，关闭logcat的抓取
            log.close()
            logO.info('END')
            q.put('q')
            break

    # 每次循化num+temp
    num += 1
    # 写入运行信息
    logO.info('开始执行第' + str(num) + '次')

    logO.info('========启动Google Movies========')
    for i in range(3):
        # 进入Google Movies播放
        adb.home(2, 0.5)
        adb.right(1)
        adb.back(1,0.5)
        adb.right(1,2)
        adb.ok(1,20)
        # 判断Google Movies是否启动成功
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

    logO.info('========启动Netflix========')
    for i in range(3):
        # 进入Netflix播放
        adb.netflix()
        time.sleep(20)
        # 判断Netflix是否启动成功
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


    logO.info('========启动HotStart========')
    # 进入HotStart播放
    adb.right(1, 2)
    adb.ok(1, 25)
    for i in range(3):
        # 判断HotStart是否启动成功
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

    logO.info('========启动ZEE5========')
    # 进入ZEE5播放
    adb.right(1, 2)
    adb.ok(1, 25)
    for i in range(3):
        # 判断ZEE5是否启动成功
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

    logO.info('========启动JioCinema========')
    # 进入JioCinema播放
    adb.right(1, 2)
    adb.ok(1, 25)
    for i in range(3):
        # 判断JioCinema是否启动成功
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

    logO.info('========启动Hungama========')
    # 进入Hungama
    adb.right(1, 2)
    adb.ok(1, 25)
    for i in range(3):
        # 判断Hungama是否启动成功
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

    logO.info('========启动prime video========')
    for i in range(3):
        # 进入prime video
        adb.prime()
        time.sleep(25)
        # 判断prime video是否启动成功
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

    logO.info('========启动YouTube========')
    for i in range(3):
        # 进入YouTube播放
        adb.youtube()
        time.sleep(20)
        # 判断YouTube是否启动成功
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

    # 进入voot播放
    adb.right(3, 1)
    adb.ok(1, 25)
    logO.info('========启动voot========')
    for i in range(3):
        # 判断voot是否启动成功
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

    # 进入ShemarooMe播放
    adb.right(1, 1)
    adb.ok(1, 25)
    logO.info('========启动ShemarooMe========')
    for i in range(3):
        # 判断ShemarooMe是否启动成功
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

    # 进入MXPLAYER TV播放
    adb.right(1, 1)
    adb.ok(1, 25)
    logO.info('========启动MXPLAYER TV========')
    for i in range(3):
        # 判断MXPLAYER TV是否启动成功
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

    logO.info('已执行完' + str(num) + '次')