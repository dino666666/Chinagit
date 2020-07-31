#_*_encoding:GBK_*_

import time
from lib.common.logcat import log
from lib.common.adbevent import adb
from lib.common.runinfo import run_log
device = '0000a091a2009e05'
path = '/home/oneplus/log/device_01/'

log = log(device=device,log_path=path)
adb = adb(device=device)
logO = run_log(logger='0000a091a2009e05',logging_path=path).getlog()

while True:
    log.open(module='test01')
    for i in range(60):
        time.sleep(60)
        result,window = adb.windows(keyword='heytap')
        logO.info(result)
        logO.info(window)
        if result:
            break
        times = adb.order("'echo [`date +%Y/%m/%d-%H:%M:%S`]'").read()
        logO.info(times)

    log.close()
    break