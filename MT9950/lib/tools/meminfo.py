#_*_encoding:GBK*_
import os
import re
class ram(object):
    def __init__(self,device):
        self.device = device
    def get(self,apkpage):
        TOTAL = 0
        NativeHeap = 0
        DalvikHeap = 0
        command = 'adb -s ' + self.device + ' shell dumpsys meminfo ' + apkpage
        print(command)
        get_ram = os.popen(command)
        read_ram = get_ram.readline()
        while read_ram:
            if 'Native Heap' in read_ram:
                try:
                    get_NativeHeap = read_ram.split(' ')
                    while '' in get_NativeHeap:
                        get_NativeHeap.remove('')
                    jude = get_NativeHeap[5]
                    print(get_NativeHeap)
                    NativeHeap = get_NativeHeap[2]
                except:
                    pass

            if 'Dalvik Heap' in read_ram:
                try:
                    get_Dalvik_Heap = read_ram.split(' ')
                    while '' in get_Dalvik_Heap:
                        get_Dalvik_Heap.remove('')
                    jude = get_Dalvik_Heap[5]
                    print(get_Dalvik_Heap)
                    DalvikHeap = get_Dalvik_Heap[2]
                except:
                    pass

            if 'TOTAL' in read_ram:
                try:
                    get_total = read_ram.split(' ')
                    while '' in get_total:
                        get_total.remove('')
                    jude = get_total[5]
                    print(get_total)
                    TOTAL = get_total[1]
                except:
                    pass

            read_ram = get_ram.readline()
        print('NativeHeap：',NativeHeap)
        print('DalvikHeap：', DalvikHeap)
        print('TOTAL：',TOTAL)
        return NativeHeap,DalvikHeap,TOTAL

# ram = ram(device_05='001AAAAJC100354DCA')
#
# print(ram.get('com.tv.sonyliv'))
#
# a = '0000040000000008'
# print(re.findall('00',a))