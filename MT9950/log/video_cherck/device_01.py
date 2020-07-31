#_*_encoding:GBK*_

import os
import time
import random
import logging
import threading
import queue

from subprocess import Popen,PIPE
from lib.common.adbevent import adb
from lib.tools.meminfo import ram
from lib.tools.procrank import procrank
from lib.tools.top import top
from lib.common.runinfo import run_log
from lib.common.logcat import log

#实例化一个队列，实现子线程与主进程之间的通讯
q=queue.Queue()



#初始化设备信息以及脚本运行过程中产生的文件保存路径
device = ' 001AAAAJC100354DCA '
path = '/home/oneplus/log/device_01/'
#定义脚本运行过程中产生的文件路径
logpath = path + 'log/'
picturepath = path + 'picture/'
runpath = path + 'runinfo/'
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

adb.order('root',type=1)
#运行脚本前，清除历史logcat
adb.order('logcat -c')
logO.info('logcat -c')
time.sleep(10)
ram = ram(device=device)
procrank = procrank(device=device)
top = top(device)
apkage = 'com.tv.sonyliv'
apkage_top = 'com.tv.sonyliv\n'

def thread_PSS():
    while True:
        times = adb.order("'echo [`date +%Y/%m/%d-%H:%M:%S`]'").read()
        PSS = ram.get(apkage)
        times_PSS = 'PSS : ' + str(times) + ':' + str(PSS)
        logO.info(times_PSS)
        time.sleep(5)

def thread_RSS():
    while True:
        times = adb.order("'echo [`date +%Y/%m/%d-%H:%M:%S`]'").read()
        getRss = procrank.Rss(apkage)
        times_RSS = 'RSS:' + str(times) + ':' + str(getRss)
        logO.info(times_RSS)
        time.sleep(5)

def thread_CPU():
    while True:
        times = adb.order("'echo [`date +%Y/%m/%d-%H:%M:%S`]'").read()
        CPU = top.cpu(apkage_top)
        times_PSS = 'CPU:' + str(times) + ':' + str(CPU)
        logO.info(times_PSS)
        time.sleep(5)

#初始化线程
thread_PSS = threading.Thread(target=thread_PSS)
thread_RSS = threading.Thread(target=thread_RSS)
thread_CPU = threading.Thread(target=thread_CPU)
#打开线程
thread_PSS.start()
thread_RSS.start()
thread_CPU.start()

num_line = 0
while True:
    command1 = 'adb -s ' + str(device) + ' shell logcat -c'
    os.popen(command1)
    time.sleep(1)
    command2 = 'adb -s ' + str(device) + ' shell logcat -b all'
    log_cat = Popen(command2, stdout=PIPE, stderr=PIPE, shell=True)
    while log_cat.poll() is None:
        log_read = log_cat.stdout.readline()
        # print(log_read)
        num_line += 1
        # print(num_line)

        if apkage in str(log_read):
            times = adb.order("'echo [`date +%Y/%m/%d-%H:%M:%S`]'").read()
            logO.info(times)
        if num_line >= 10000:
            num_line = 0
            print()
            print()
            print()
            break