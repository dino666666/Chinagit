#_*_encoding:GBK_*_

import os,time

while True:
    os.system('adb -s 0000040000000000 shell input keyevent KEYCODE_ENTER')
    time.sleep(60)