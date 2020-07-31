#_*_encoding:utf-8_*_
import time,subprocess,os
class log(object):
    #实时获取日志
    def __init__(self,device,log_path):
        self.device=device
        self.log_path=log_path
    def open(self,module):
    #开启日志抓取
        lt=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        logpath=self.log_path+module+'-'+lt+'.log'
        op = open(logpath, 'a', encoding='utf-8', errors='ignore')
        command2 = 'adb -s ' + self.device + ' logcat'
        self.log=subprocess.Popen(command2,stdout=op,stderr=subprocess.PIPE,shell=True,close_fds=True)
        print(self.log.pid)

    def close(self):
    #关闭日志抓取device
        process = os.popen('ps -ef | grep -i ' + self.device)
        pid_name = process.readline()
        while pid_name:
            time.sleep(1)
            print(pid_name)
            for i in pid_name.split(' '):
                try:
                    pid=int(i)
                    print(pid)
                    os.system('kill -9 %s'%pid)
                    break
                except:
                    pass
            pid_name = process.readline()
        print('logcat end')
        # devNull=open(os.devnull,'w')
        # pid=str(int(self.log.pid)+temp)
        # a=subprocess.Popen('kill -9 %s'%self.log.pid,stdout=devNull,stderr=subprocess.PIPE,shell=True,close_fds=True)
        # print(self.log.pid)
        # # a = subprocess.Popen('taskkill /t/f/pid %s' % self.log.pid, stdout=devNull, stderr=subprocess.PIPE, shell=True)
        # time.sleep(2)
        # self.log.terminate()
        # a.wait()
        # a.terminate()
        # time.sleep(30)
        #
        # os.system('kill -9 %s' %pid)
        # print(pid)