#_*_encoding:GBK*_
import os,time,subprocess,logging
logging.basicConfig(level=logging.DEBUG,format=' %(asctime)s - %(levelname)s - %(message)s')
def cycle(num,times,command):
    for i in range(0,num):
        os.system(command)
        # logging.info(command)
        time.sleep(times)

class adb(object):
    def __init__(self,device):
        self.device=device

    def up(self,num=1,times=0,type=0):
        if type==0:
            up = 'adb -s ' + self.device + ' shell input keyevent 19'
            cycle(num,times,up)
        else:
            up = 'adb -s ' + self.device + ' shell input keyevent --longpress 19'
            cycle(num,times,up)

    def down(self,num=1,times=0,type=0):
        if type==0:
            down = 'adb -s ' + self.device + ' shell input keyevent 20'
            cycle(num,times,down)
        else:
            down = 'adb -s ' + self.device + ' shell input keyevent --longpress 20'
            cycle(num,times,down)

    def right(self,num=1,times=0,type=0):
        if type==0:
            right='adb -s '+self.device+' shell input keyevent 22'
            cycle(num,times,right)
        else:
            right = 'adb -s ' + self.device + ' shell input keyevent --longpress 22'
            cycle(num,times,right)

    def left(self,num=1,times=0,type=0):
        if type==0:
            left='adb -s '+self.device+' shell input keyevent 21'
            cycle(num,times,left)
        else:
            left = 'adb -s ' + self.device + ' shell input keyevent --longpress 21'
            cycle(num,times,left)

    def ok(self,num=1,times=0):
        ok = 'adb -s ' + self.device + ' shell input keyevent 23'
        cycle(num,times,ok)

    def back(self,num=1,times=0):
        back='adb -s '+self.device+' shell input keyevent 4'
        cycle(num,times,back)

    # tab键
    def tab(self):
        tab = 'adb -s ' + self.device + ' shell input keyevent 61'
        os.system(tab)

    # enter键
    def enter(self):
        enter = 'adb -s ' + self.device + ' shell input keyevent 66'
        os.system(enter)

    def home(self,num=1,times=0):
        home='adb -s '+self.device+' shell input keyevent 3'
        cycle(num,times,home)

    def menu(self,num=1,times=0,type=0):
        if type==0:
            menu='adb -s '+self.device+' shell input keyevent 82'
            cycle(num,times,menu)
        else:
            menu='adb -s '+self.device+' shell input keyevent --longpress 82'
            os.system(menu)

    # def oneplus(self,type=0):
    #     if type==0:
    #         oneplus='adb -s ' + self.device_05 + ' shell input keyevent 132'
    #         os.system(oneplus)
    #     else:
    #         command1 = 'adb -s ' + self.device_05 + ' shell sendevent /dev/input/event2 temp 60 0'
    #         os.system(command1)
    #         time.sleep(0.5)
    #         command2='adb -s ' + self.device_05 + ' shell sendevent /dev/input/event2 temp 60 temp'
    #         os.system(command2)
    #         time.sleep(0.5)
    #         command3='adb -s ' + self.device_05 + ' shell sendevent /dev/input/event2 0 0 0'
    #         os.system(command3)
    #         time.sleep(temp.5)
    #         command4 = 'adb -s ' + self.device_05 + ' shell sendevent /dev/input/event2 temp 60 0'
    #         os.system(command4)
    #         time.sleep(0.5)
    #         command5 = 'adb -s ' + self.device_05 + ' shell sendevent /dev/input/event2 0 0 0'
    #         os.system(command5)

    def oneplus(self,type=0):
        if type==0:
            oneplus='adb -s ' + self.device + ' shell input keyevent 132'
            os.system(oneplus)
        else:
            command1 = 'adb -s ' + self.device + ' shell sendevent /dev/input/event0 temp 60 0'
            os.system(command1)
            time.sleep(0.5)
            command2='adb -s ' + self.device + ' shell sendevent /dev/input/event0 temp 60 temp'
            os.system(command2)
            time.sleep(0.5)
            command3='adb -s ' + self.device + ' shell sendevent /dev/input/event0 0 0 0'
            os.system(command3)
            time.sleep(1.5)
            command4 = 'adb -s ' + self.device + ' shell sendevent /dev/input/event0 temp 60 0'
            os.system(command4)
            time.sleep(0.5)
            command5 = 'adb -s ' + self.device + ' shell sendevent /dev/input/event0 0 0 0'
            os.system(command5)

    def netflix(self):
        netflix = 'adb -s ' + self.device + ' shell input keyevent 265'
        os.system(netflix)

    def youtube(self):
        youtube = 'adb -s ' + self.device + ' shell input keyevent 135'
        os.system(youtube)

    def prime(self):
        prime = 'adb -s ' + self.device + ' shell input keyevent 133'
        os.system(prime)

    def inputs(self):
        inputs = 'adb -s ' + self.device + ' shell input keyevent 136'
        os.system(inputs)

    def text(self,text):
        te='adb -s '+self.device+' shell "input text '+text+'"'
        os.system(te)

    def app_start(self,times=2,keyword='com',package=None):
        start='adb -s '+self.device+' shell am start -W '+package
        os.popen(start)
        time.sleep(times)
        command = 'adb -s ' + self.device + ' shell "dumpsys window windows | grep mCurrent"'
        key = os.popen(command).read()
        if keyword in key:
            return True,key
        else:
            return False,key

    def app_stop(self,times=2,keyword='com',package=None):
        stop='adb -s '+self.device+' shell am force-stop '+package
        os.popen(stop)
        time.sleep(times)
        command = 'adb -s ' + self.device + ' shell "dumpsys window windows | grep mCurrent"'
        key = os.popen(command).read()
        if keyword in key:
            return False, key
        else:
            return True, key

    def screencap(self,path=None,module=None,type=0):
        if type == 0:
            screencap='adb -s '+self.device+' exec-out screencap -p > '+path
            os.system(screencap)
            logging.info(screencap)
        else:
            pt = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
            name = str(path) + str(module) + str(pt) +'.png'
            screencap = 'adb -s ' + self.device + ' exec-out screencap -p > ' + name
            os.system(screencap)
            return name

    def screenrecord(self,times=None,path=None):
        screenrecord='adb -s '+self.device+' shell screenrecord --time-limit '+times+path
        os.system(screenrecord)
        logging.info(screenrecord)

    def pull(self,adb_path,local_path):
        pull='adb -s '+self.device+' pull '+adb_path+' '+local_path
        os.system(pull)
        logging.info(pull)

    def push(self,adb_path,local_path):
        push='adb -s '+self.device+' push '+local_path+' '+adb_path
        os.system(push)
        logging.info(push)

    def windows(self,keyword):
        command='adb -s '+self.device+' shell "dumpsys window windows | grep mCurrent"'
        key=os.popen(command).read()
        # logging.info(key)
        if keyword in key:
            return True,key
        else:
            return False,key

    def order(self,command,type=0):
        if type==0:
            command='adb -s '+self.device+' shell '+ command
            p=os.popen(command)
            # logging.info(command)
            return p
        else:
            command = 'adb -s ' + self.device + ' ' + command
            p=os.popen(command)
            # logging.info(command)
            return p

# adb("001AAAAJC10045D45D").windows("com")