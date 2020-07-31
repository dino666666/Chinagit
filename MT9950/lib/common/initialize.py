#_*_encoding:GBK_*_
import os,time
def initialize(device):
    time.sleep(1)
    command2 = 'adb -s ' + device + ' shell input keyevent 4'
    for i in range(0,5):
        os.system(command2)
    command1='adb -s '+device+' shell am start com.google.android.tvlauncher/.MainActivity'
    os.system(command1)
    time.sleep(1)
    command2='adb -s '+device+' shell input keyevent 4'
    for i in range(0,3):
        os.system(command2)
    time.sleep(1)
    command3='adb -s '+device+' shell input keyevent 21'
    for i in range(0,3):
        os.system(command3)
    time.sleep(1)
    command4='adb -s '+device+' shell input keyevent 22'
    os.system(command4)