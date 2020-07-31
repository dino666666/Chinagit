# coding=gbk
import os
import re
import time
#�����ǰ�ڴ�ʹ���������getTotalRam
class Performance(object):
    def __init__(self,device):
        self.device=device
    def getTotalRam(self):
        # �鿴��ǰ�ڴ�ʹ����������ж�ȡ���һ��Total���ڴ�
        lines = os.popen("adb -s "+ self.device +" shell cat /proc/meminfo").readlines()
        total = "MemTotal"
        free = "MemFree"
        lis = []
        fre = []
        for line in lines:   #���ڴ�
            if re.findall(total,line):  #���б�����ҵ���һ�� ����TOTAL
                lis = line.split(' ')  #�����а��ո�ָ��һ��list�б�
                while '' in lis:  #��list�б��еĿ�Ԫ��ɾ��
                    lis.remove('')
        for line in lines:   #ʣ������ڴ�
            if re.findall(free, line):  # ���б�����ҵ���һ�� ����TOTAL
                fre = line.split(' ')  # �����а��ո�ָ��һ��list�б�
                while '' in fre:  # ��list�б��еĿ�Ԫ��ɾ��
                    fre.remove('')
        # �ڴ�kbת����G  1ǧ���ֽ�(gb)=1048576ǧ�ֽ�(kb)  Ҳ����1024��2�η�
        ramused = (int(lis[1]) - int(fre[1])) /  1024**2#�ܹ��ڴ� - �����ڴ� = ��ʹ���ڴ�
        # print(ramused)
        # useda = ramused / 1024**2
        # print(useda)
        return round(ramused,2)  # ����ʹ�õ��ڴ淵�س�ȥ������2λС��
    #�����ǰϵͳcpuʹ�����
    def getCpu(self):
        #�鿴��ǰcupʹ����������ж�ȡ���һ���ܵ�cpuʹ���������¼�ɵ�ǰcpuʹ�����
        li = os.popen("adb -s "+ self.device +" shell top -k %CPU -d 15 -n temp").readlines()
        name = 'idle'
        for line in li:
            if re.findall(name,line):  #������cpu�б�����ҵ�����sys
                line = line.split(' ')  #�����а��ո�ָ��һ��list�б�
                while '' in line:  #��list�б��еĿ�Ԫ��ɾ��
                    line.remove('')
                total = line[0].split('%') #�ܹ���CPU�ռ�
                idle = line[4].split('%')#idle ��ȡʣ�࣬�����ڴ�
                used = float(total[0]) - float(idle[0])  #�ܹ��ڴ� -  ʣ���ڴ棬�����ڴ� = ��ʹ���ڴ�
                return float(used) #ȥ���ٷֺţ�����һ��float  # ���б��еĵ�һ�����ݣ�Ҳ����Total�ܵ�CPUʹ����������س�ȥ��
    #����fps���л���
    def load_surround(self):
        #ȡ��Զ�λ�㼶
        path = os.path.abspath(os.path.join(os.getcwd(), '..'))
        print(path)
        # ��ȡfps.sh���е��ļ�
        os.system("adb -s " + self.device + " push "+path+"\OUT\FPS_Test_1.6\\fps.sh /sdcard")
        #��������ļ�Ȩ��
        os.system("adb -s " + self.device + " push "+path+"\OUT\FPS_Test_1.6\\busybox /sdcard")
        os.system("adb -s " + self.device + " shell chmod 777 /sdcard")
        time.sleep(1)
        os.system("adb -s " + self.device + " shell cd /sdcard cp busybox  /data/local/tmp")
        time.sleep(1)
        os.system("adb -s " + self.device + " shell cd /data/local/tmp chmod 777  busybox")
    #��ȡ�����л�ʱFPS����
    def getfps(self):
        # ���� ���ܲ��Թ���shell�ű�д�Ķ�ȡ����ǰ�򿪵Ĵ��ڵ�fps���ݡ�
        # ��ȡ�����л�ʱ�������ȵ�fps
        devices = os.popen("adb -s " + self.device + " shell  sh /sdcard/fps.sh -t 60 -k 1000/60")
        dsv = devices.readline()  # ���ж�ȡfps����
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
        print("�����res:%s" % result)
        return result
