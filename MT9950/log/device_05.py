#_*_encoding:GBK_*_

import time
from lib.common.logcat import log
from lib.common.adbevent import adb
from lib.common.runinfo import run_log
device = '001AAAAJC100354DCA'
path = '/home/oneplus/log/device_05/'

log = log(device=device,log_path=path)
adb = adb(device=device)
logO = run_log(logger='011000AL3J0031CE0A',logging_path=path).getlog()

while True:

    log.open(module='youtube5915')
    for i in range(60):
        time.sleep(180)
        result,window = adb.windows(keyword='youtube')
        logO.info(result)
        logO.info(window)
        times = adb.order("'echo [`date +%Y/%m/%d-%H:%M:%S`]'").read()
        logO.info(times)

    log.close()