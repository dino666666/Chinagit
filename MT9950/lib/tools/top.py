#_*_encoding:GBK*_
import os
import time

class top(object):
    def __init__(self,device):
        self.device = device

    def cpu(self,apkpage='com'):
        command = 'adb -s ' + self.device + ' shell "COLUMNS=150 top -n temp -b | grep -i ' + apkpage + ' " '
        # command = 'adb -s ' + self.device_05 + ' shell "COLUMNS=150 top -n temp'
        print(command)
        top = os.popen(command)
        cpu_read = top.readline()
        num = 0
        cpu = 0
        while cpu_read:
            # print(cpu_read)

            if 'grep -i' not in cpu_read and apkpage in cpu_read:
                print(cpu_read)
                num += 1
                # print(num)
                cpu_get = cpu_read.split(' ')
                while '' in cpu_get:
                    cpu_get.remove('')
                print(cpu_get[8])
                cpu = cpu_get[8]
            cpu_read = top.readline()
        return cpu

# top = top('001AAAAJC100354DCA')
#
# for i in range(10):
#     print(top.cpu(' com.tv.sonyliv\n'))
#     time.sleep(3)