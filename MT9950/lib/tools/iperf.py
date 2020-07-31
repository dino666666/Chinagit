#_*_encoding:GBK*_
import os,time,re,subprocess
class iperf(object):
    def __init__(self,device,iperf_path,save_path):#传参：device_test id,iperf 路径，device目录路径
        #iperf2=iperf(device_test='0000a091a200020d',iperf_path='C:\\Users\\602836\\Downloads\\iperf-2.0.5-win32',device_number='device_01')
        self.device=device
        self.iperf_path=iperf_path
        self.save_path=save_path
    def get_ip(self):#获取WindowsIP和TVIP,return windowsip,androidip
        os.system('taskkill /f /t /im iperf.exe')
        command3 = 'adb -s ' + self.device + ' shell killall -HUP iperf'
        os.system(command3)
        a=os.popen('ipconfig')#在Windows下获取ipconfig内容
        b=a.readline()
        flag=0
        while b:
            c=re.search('WLAN',b)#获得WiFi网络内容
            if c!=None:
                flag=1
            if flag==1:
                d=re.search('IPv4',b)#获取WiFiIP
                if d!=None:
                    flag=0
                    windowsip=b.split(' ')[-1].split('\n')[0]#得到WiFiIP地址
            b=a.readline()
        flag=0
        command='adb -s '+self.device+' shell ifconfig'
        a=os.popen(command)#在Android下获取ifconfig内容
        b=a.readline()
        while b:
            c=re.search('wlan0',b)#获取无线网卡信息
            if c!=None:
                flag=1
            if flag==1:
                d=re.search('inet addr',b)#获取无线网卡IP地址
                if d!=None:
                    flag=0
                    androidip=b.split(':')[1].split(' ')[0]
            b=a.readline()#获取到的无线网卡IP地址
        return windowsip,androidip
    def push_iperf(self):#将iperf工具推送到sdcard目录下
        command='adb -s '+self.device+' push '+self.iperf_path+' /sdcard'
        os.system(command)
    def tcp(self,windowsip):#使用TCP协议获取当前带宽、网路是否连接正常（丢包），并返回一个不带单位的带宽，return Unit,Odds,num
        #传参：widowsipip
        os.system('taskkill /f /t /im iperf.exe')
        command3 = 'adb -s ' + self.device + ' shell killall -HUP iperf'
        os.system(command3)
        server_path=self.save_path+'\\tcpservesr.txt'#存放tcp服务端返回的内容
        server_op=open(server_path,'w',encoding='utf-8',errors='ignore')
        command1='cd '+self.iperf_path+'&iperf -s -p 5001'
        server=subprocess.Popen(command1,shell=True,stdout=server_op,stderr=subprocess.PIPE)#启动tcp服务端
        time.sleep(2)
        command2='adb -s '+self.device+' shell iperf -c '+windowsip+' -i temp -t 10 -p 5001'
        client=os.popen(command2)#启动tcp客户端
        clientinfo=client.readline()
        num=0
        null=0
        while clientinfo:#遍历客户端返回的内容
            print(clientinfo)
            if 'sec' in clientinfo:#统计总发包数
                num+=1
            if 'null' in clientinfo:#统计丢包数
                null+=1
            clientinfo=client.readline()
        try:
            odds=null/num#统计丢包率
            print('丢包率:',odds*100,"%")
            Odds='丢包:'+str(odds*100)+"%"
        except:#判断网络是否连接
            print('connect failed: Network is unreachable')
        time.sleep(3)
        devNull=open(os.devnull,'w')
        a=subprocess.Popen('taskkill /t/f/pid %s'%server.pid,shell=True,stdout=devNull,stderr=subprocess.PIPE)
        os.system('taskkill /f /t /im iperf.exe')
        server_op.close()
        server.terminate()
        server.kill()
        a.wait()
        a.terminate()
        time.sleep(1)
        server_op=open(server_path,'r',encoding='utf-8',errors='ignore')
        read=server_op.readline()
        while read:#遍历tcp服务端内容
            if 'sec' in read:#寻找带宽、丢包率的内容信息
                num=read.split(' ')[-2]#输出带宽数值
                unit=read.split(' ')[-1].split('/')[0]#输出带宽单位
                print('带宽:',num+unit)
                Unit=num+unit#一个完整的带宽显示，数值+单位
            read=server_op.readline()
        server_op.close()
        return Unit,Odds,num
    def udp_up(self,windowsip,num):#使用udp协议获取指定带宽的上行丢包率odds、抖动Jitter,return odds,Jitter
        #传参：WindowsIP，不带单位宽带数值
        # os.system('taskkill /f /t /im iperf.exe')
        # command3 = 'adb -s ' + self.device_test + ' shell killall -HUP iperf'
        # os.system(command3)
        print('UDP上行')
        server_path=self.save_path+'\\udp_up_servesr.txt'#存储udp上行服务端（Windows下）返回的内容
        server_op=open(server_path,'w',encoding='utf-8',errors='ignore')
        command1='cd '+self.iperf_path+'&iperf -s -p 5001 -u'
        server=subprocess.Popen(command1,shell=True,stdout=server_op,stderr=subprocess.PIPE)#启动udp上行服务端
        time.sleep(2)
        command2='adb -s '+self.device+' shell iperf -c '+windowsip+' -p 5001 -i temp -t 10 -u -b'+num+'M'
        client=os.popen(command2)#启动udp上行客户端
        clientinfo=client.readline()
        while clientinfo:#遍历udp上行客户端返回的内容
            if '%' in clientinfo:#找到带有丢包率odds、抖动Jitter的内容信息
                odds=clientinfo.split(' ')[-1].split(')')[0].split('(')[-1]#将丢包率切割出来，格式化
                Jitter = clientinfo.split(' ')[14] + clientinfo.split(' ')[15]#将抖动切割出来，格式化
                print('up丢包率:', odds)
                print('upJitter:', Jitter)
            print(clientinfo)
            clientinfo=client.readline()
        # os.system('taskkill /f /t /im iperf.exe')
        server.terminate()
        return odds,Jitter
    def udp_down(self,androidip,num):#使用udp协议获取指定带宽的下行丢包率odds、抖动Jitter,return odds,Jitter，return odds,Jitter
        #传参：androidIP，一个不带单位的宽带数值
        os.system('taskkill /f /t /im iperf.exe')
        command3 = 'adb -s ' + self.device + ' shell killall -HUP iperf'
        os.system(command3)
        print('UDP下行')
        server_path=self.save_path+'udp_down_servesr.txt'#存储udp下行服务端返回的内容
        client_path=self.save_path+'\\udp_down_client.txt'#存储udp下行客户端返回的内容
        server_op=open(server_path,'w',encoding='utf-8',errors='ignore')
        client_op=open(client_path,'w',encoding='utf-8',errors='ignore')
        command1='adb -s '+self.device+' shell iperf -s -u -p 5001'
        server=subprocess.Popen(command1,stdout=server_op,stderr=server_op)#启动udp下行服务端，Android下
        time.sleep(2)
        command2='cd '+self.iperf_path+'&iperf -c '+androidip+' -i temp -t 10 -u -b'+num+'M'
        client=subprocess.Popen(command2,shell=True,stdout=client_op,stderr=client_op,stdin=client_op)#启动udp下行客户端，windo下
        client.wait()
        server_op.close()
        client_op.close()
        client_op=open(client_path,'r',encoding='utf-8',errors='ignore')
        clientinfo=client_op.readline()
        while clientinfo:#遍历客户端返回的内容
                if '%' in clientinfo:#找到带有丢包率、抖动信息的内容
                    print(clientinfo)
                    odds=clientinfo.split(' ')[-1].split(')')[0].split('(')[-1]#将udp下行丢包率切割出来，格式化
                    Jitter = clientinfo.split(' ')[14] + clientinfo.split(' ')[15]#将udp下行抖动切割出来，格式化
                    print('down丢包率:',odds)
                    print('downJitter:',Jitter)
                print(clientinfo)
                clientinfo=client_op.readline()
        os.system('taskkill /f /t /im iperf.exe')
        command3='adb -s '+self.device+' shell killall -HUP iperf'
        os.system(command3)
        server_op.close()
        client_op.close()
        server.terminate()
        return odds,Jitter
def run_iperf2(device,iperf_path,save_path):
    #iperf2=run_iperf2(device_test='0000a091a200020d',iperf_path='C:\\Users\\602836\\Downloads\\iperf-2.0.5-win32',device_number='device_01')
    iperf2=iperf(device=device,iperf_path=iperf_path,save_path=save_path)
    # iperf2=iperf(device_test='0000a091a200020d',iperf_path='C:\\Users\\602836\\Downloads\\iperf-2.0.5-win32',device_number='device_01')
    for i in range(1,4):
        flag=1
        try:
            iperf2.push_iperf()
            time.sleep(10)
        except:
            print('iperf路径错误')
        try:
            windowsip,androidip=iperf2.get_ip()
        except:
            print('windows或android未连接WiFi网络')
            flag=0
        try:
            unit,odds,num=iperf2.tcp(windowsip)
        except:
            print('当前Windows和Android可能没有连接同一个WiFi')
            flag=0
        try:
            udp_up_odds,udp_up_Jitter=iperf2.udp_up(windowsip,num)
        except:
            print('当前Windows和Android可能没有连接同一个WiFi')
            flag=0
        try:
            udp_down_odds,udp_down_Jitter=iperf2.udp_down(androidip,num)
        except:
            print('当前Windows和Android可能没有连接同一个WiFi')
            flag=0
        if flag==1:
            break
        else:
            print('重新测试中，第',i,'次（重试超过三次则放弃），请耐心等候。。。')
            time.sleep(10)
    try:
        print('windowsip:',windowsip)
        print('androidip:',androidip)
        print('带宽:',unit)
        print('上行丢包:',udp_up_odds)
        print('上行抖动:',udp_up_Jitter)
        print('下行丢包:',udp_down_odds)
        print('下行抖动:',udp_down_Jitter)
        return windowsip, androidip, unit, udp_up_odds, udp_up_Jitter, udp_down_odds, udp_down_Jitter
    except:
        print('====请排查网路错误再重试====')
# iperf2=run_iperf2(device_test='0000a091a200001f',iperf_path='C:\\Users\\602836\\Downloads\\iperf-2.0.5-win32',save_path='C:\\Project_TV\\device_02\\files_data\\')
# print(iperf2)