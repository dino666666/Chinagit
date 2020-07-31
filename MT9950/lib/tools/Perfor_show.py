# coding=gbk
import os
import re
import time
#输出当前内存使用情况方法getTotalRam
class Performance(object):
    def __init__(self,device):
        self.device=device
    def getTotalRam(self):
        # 查看当前内存使用情况，逐行读取最后一个Total总内存
        lines = os.popen("adb -s "+ self.device +" shell cat /proc/meminfo").readlines()
        total = "MemTotal"
        free = "MemFree"
        lis = []
        fre = []
        for line in lines:   #总内存
            if re.findall(total,line):  #在列表里查找到这一行 包含TOTAL
                lis = line.split(' ')  #将这行按空格分割成一个list列表
                while '' in lis:  #将list列表中的空元素删除
                    lis.remove('')
        for line in lines:   #剩余空闲内存
            if re.findall(free, line):  # 在列表里查找到这一行 包含TOTAL
                fre = line.split(' ')  # 将这行按空格分割成一个list列表
                while '' in fre:  # 将list列表中的空元素删除
                    fre.remove('')
        # 内存kb转换成G  1千兆字节(gb)=1048576千字节(kb)  也就是1024的2次方
        ramused = (int(lis[1]) - int(fre[1])) /  1024**2#总共内存 - 空闲内存 = 已使用内存
        # print(ramused)
        # useda = ramused / 1024**2
        # print(useda)
        return round(ramused,2)  # 将已使用的内存返回出去，保留2位小数
    #输出当前系统cpu使用情况
    def getCpu(self):
        #查看当前cup使用情况，逐行读取最后一行总的cpu使用情况，记录成当前cpu使用情况
        li = os.popen("adb -s "+ self.device +" shell top -k %CPU -d 15 -n temp").readlines()
        name = 'idle'
        for line in li:
            if re.findall(name,line):  #在所有cpu列表里查找到包含sys
                line = line.split(' ')  #将这行按空格分割成一个list列表
                while '' in line:  #将list列表中的空元素删除
                    line.remove('')
                total = line[0].split('%') #总共的CPU空间
                idle = line[4].split('%')#idle 获取剩余，空闲内存
                used = float(total[0]) - float(idle[0])  #总共内存 -  剩余内存，空闲内存 = 已使用内存
                return float(used) #去掉百分号，返回一个float  # 将列表中的第一个数据，也就是Total总的CPU使用情况，返回出去。
    #配置fps运行环境
    def load_surround(self):
        #取相对定位层级
        path = os.path.abspath(os.path.join(os.getcwd(), '..'))
        print(path)
        # 获取fps.sh运行的文件
        os.system("adb -s " + self.device + " push "+path+"\OUT\FPS_Test_1.6\\fps.sh /sdcard")
        #给传入的文件权限
        os.system("adb -s " + self.device + " push "+path+"\OUT\FPS_Test_1.6\\busybox /sdcard")
        os.system("adb -s " + self.device + " shell chmod 777 /sdcard")
        time.sleep(1)
        os.system("adb -s " + self.device + " shell cd /sdcard cp busybox  /data/local/tmp")
        time.sleep(1)
        os.system("adb -s " + self.device + " shell cd /data/local/tmp chmod 777  busybox")
    #获取窗口切换时FPS数据
    def getfps(self):
        # 根据 性能测试工具shell脚本写的读取到当前打开的窗口的fps数据。
        # 获取窗口切换时，流畅度的fps
        devices = os.popen("adb -s " + self.device + " shell  sh /sdcard/fps.sh -t 60 -k 1000/60")
        dsv = devices.readline()  # 逐行读取fps数据
        log = 0
        result = ""
        while dsv:
            if dsv is not None:
                m = re.search('FPS',dsv)
                if m is not None:
                    log = 1
                else:
                    log = 2
                print(log)
            try:
                if log == 2:
                    log = 0
                    result = dsv.split(' ')[-1].split('\t')[1]
                    pid = '"ps -fe|grep fps.sh | awk '"'{print $2}'"' | head -n temp"'
                    shpid=os.system('adb -s '+self.device+' shell '+pid+'')
                    shpd = str(shpid)
                    os.system("adb -s "+self.device+" shell kill -9 " + shpd + "")
                    print(shpd)
            except:
                None
            if result != "":
                break
            dsv = devices.readline()
        print("这个是res:%s" % result)
        return result
