#_*_encoding:GBK*_
import os,time,re,subprocess
class iperf(object):
    def __init__(self,device,iperf_path,save_path):#���Σ�device_test id,iperf ·����deviceĿ¼·��
        #iperf2=iperf(device_test='0000a091a200020d',iperf_path='C:\\Users\\602836\\Downloads\\iperf-2.0.5-win32',device_number='device_01')
        self.device=device
        self.iperf_path=iperf_path
        self.save_path=save_path
    def get_ip(self):#��ȡWindowsIP��TVIP,return windowsip,androidip
        os.system('taskkill /f /t /im iperf.exe')
        command3 = 'adb -s ' + self.device + ' shell killall -HUP iperf'
        os.system(command3)
        a=os.popen('ipconfig')#��Windows�»�ȡipconfig����
        b=a.readline()
        flag=0
        while b:
            c=re.search('WLAN',b)#���WiFi��������
            if c!=None:
                flag=1
            if flag==1:
                d=re.search('IPv4',b)#��ȡWiFiIP
                if d!=None:
                    flag=0
                    windowsip=b.split(' ')[-1].split('\n')[0]#�õ�WiFiIP��ַ
            b=a.readline()
        flag=0
        command='adb -s '+self.device+' shell ifconfig'
        a=os.popen(command)#��Android�»�ȡifconfig����
        b=a.readline()
        while b:
            c=re.search('wlan0',b)#��ȡ����������Ϣ
            if c!=None:
                flag=1
            if flag==1:
                d=re.search('inet addr',b)#��ȡ��������IP��ַ
                if d!=None:
                    flag=0
                    androidip=b.split(':')[1].split(' ')[0]
            b=a.readline()#��ȡ������������IP��ַ
        return windowsip,androidip
    def push_iperf(self):#��iperf�������͵�sdcardĿ¼��
        command='adb -s '+self.device+' push '+self.iperf_path+' /sdcard'
        os.system(command)
    def tcp(self,windowsip):#ʹ��TCPЭ���ȡ��ǰ������·�Ƿ�������������������������һ��������λ�Ĵ���return Unit,Odds,num
        #���Σ�widowsipip
        os.system('taskkill /f /t /im iperf.exe')
        command3 = 'adb -s ' + self.device + ' shell killall -HUP iperf'
        os.system(command3)
        server_path=self.save_path+'\\tcpservesr.txt'#���tcp����˷��ص�����
        server_op=open(server_path,'w',encoding='utf-8',errors='ignore')
        command1='cd '+self.iperf_path+'&iperf -s -p 5001'
        server=subprocess.Popen(command1,shell=True,stdout=server_op,stderr=subprocess.PIPE)#����tcp�����
        time.sleep(2)
        command2='adb -s '+self.device+' shell iperf -c '+windowsip+' -i temp -t 10 -p 5001'
        client=os.popen(command2)#����tcp�ͻ���
        clientinfo=client.readline()
        num=0
        null=0
        while clientinfo:#�����ͻ��˷��ص�����
            print(clientinfo)
            if 'sec' in clientinfo:#ͳ���ܷ�����
                num+=1
            if 'null' in clientinfo:#ͳ�ƶ�����
                null+=1
            clientinfo=client.readline()
        try:
            odds=null/num#ͳ�ƶ�����
            print('������:',odds*100,"%")
            Odds='����:'+str(odds*100)+"%"
        except:#�ж������Ƿ�����
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
        while read:#����tcp���������
            if 'sec' in read:#Ѱ�Ҵ��������ʵ�������Ϣ
                num=read.split(' ')[-2]#���������ֵ
                unit=read.split(' ')[-1].split('/')[0]#�������λ
                print('����:',num+unit)
                Unit=num+unit#һ�������Ĵ�����ʾ����ֵ+��λ
            read=server_op.readline()
        server_op.close()
        return Unit,Odds,num
    def udp_up(self,windowsip,num):#ʹ��udpЭ���ȡָ����������ж�����odds������Jitter,return odds,Jitter
        #���Σ�WindowsIP��������λ�����ֵ
        # os.system('taskkill /f /t /im iperf.exe')
        # command3 = 'adb -s ' + self.device_test + ' shell killall -HUP iperf'
        # os.system(command3)
        print('UDP����')
        server_path=self.save_path+'\\udp_up_servesr.txt'#�洢udp���з���ˣ�Windows�£����ص�����
        server_op=open(server_path,'w',encoding='utf-8',errors='ignore')
        command1='cd '+self.iperf_path+'&iperf -s -p 5001 -u'
        server=subprocess.Popen(command1,shell=True,stdout=server_op,stderr=subprocess.PIPE)#����udp���з����
        time.sleep(2)
        command2='adb -s '+self.device+' shell iperf -c '+windowsip+' -p 5001 -i temp -t 10 -u -b'+num+'M'
        client=os.popen(command2)#����udp���пͻ���
        clientinfo=client.readline()
        while clientinfo:#����udp���пͻ��˷��ص�����
            if '%' in clientinfo:#�ҵ����ж�����odds������Jitter��������Ϣ
                odds=clientinfo.split(' ')[-1].split(')')[0].split('(')[-1]#���������и��������ʽ��
                Jitter = clientinfo.split(' ')[14] + clientinfo.split(' ')[15]#�������и��������ʽ��
                print('up������:', odds)
                print('upJitter:', Jitter)
            print(clientinfo)
            clientinfo=client.readline()
        # os.system('taskkill /f /t /im iperf.exe')
        server.terminate()
        return odds,Jitter
    def udp_down(self,androidip,num):#ʹ��udpЭ���ȡָ����������ж�����odds������Jitter,return odds,Jitter��return odds,Jitter
        #���Σ�androidIP��һ��������λ�Ŀ����ֵ
        os.system('taskkill /f /t /im iperf.exe')
        command3 = 'adb -s ' + self.device + ' shell killall -HUP iperf'
        os.system(command3)
        print('UDP����')
        server_path=self.save_path+'udp_down_servesr.txt'#�洢udp���з���˷��ص�����
        client_path=self.save_path+'\\udp_down_client.txt'#�洢udp���пͻ��˷��ص�����
        server_op=open(server_path,'w',encoding='utf-8',errors='ignore')
        client_op=open(client_path,'w',encoding='utf-8',errors='ignore')
        command1='adb -s '+self.device+' shell iperf -s -u -p 5001'
        server=subprocess.Popen(command1,stdout=server_op,stderr=server_op)#����udp���з���ˣ�Android��
        time.sleep(2)
        command2='cd '+self.iperf_path+'&iperf -c '+androidip+' -i temp -t 10 -u -b'+num+'M'
        client=subprocess.Popen(command2,shell=True,stdout=client_op,stderr=client_op,stdin=client_op)#����udp���пͻ��ˣ�windo��
        client.wait()
        server_op.close()
        client_op.close()
        client_op=open(client_path,'r',encoding='utf-8',errors='ignore')
        clientinfo=client_op.readline()
        while clientinfo:#�����ͻ��˷��ص�����
                if '%' in clientinfo:#�ҵ����ж����ʡ�������Ϣ������
                    print(clientinfo)
                    odds=clientinfo.split(' ')[-1].split(')')[0].split('(')[-1]#��udp���ж������и��������ʽ��
                    Jitter = clientinfo.split(' ')[14] + clientinfo.split(' ')[15]#��udp���ж����и��������ʽ��
                    print('down������:',odds)
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
            print('iperf·������')
        try:
            windowsip,androidip=iperf2.get_ip()
        except:
            print('windows��androidδ����WiFi����')
            flag=0
        try:
            unit,odds,num=iperf2.tcp(windowsip)
        except:
            print('��ǰWindows��Android����û������ͬһ��WiFi')
            flag=0
        try:
            udp_up_odds,udp_up_Jitter=iperf2.udp_up(windowsip,num)
        except:
            print('��ǰWindows��Android����û������ͬһ��WiFi')
            flag=0
        try:
            udp_down_odds,udp_down_Jitter=iperf2.udp_down(androidip,num)
        except:
            print('��ǰWindows��Android����û������ͬһ��WiFi')
            flag=0
        if flag==1:
            break
        else:
            print('���²����У���',i,'�Σ����Գ���������������������ĵȺ򡣡���')
            time.sleep(10)
    try:
        print('windowsip:',windowsip)
        print('androidip:',androidip)
        print('����:',unit)
        print('���ж���:',udp_up_odds)
        print('���ж���:',udp_up_Jitter)
        print('���ж���:',udp_down_odds)
        print('���ж���:',udp_down_Jitter)
        return windowsip, androidip, unit, udp_up_odds, udp_up_Jitter, udp_down_odds, udp_down_Jitter
    except:
        print('====���Ų���·����������====')
# iperf2=run_iperf2(device_test='0000a091a200001f',iperf_path='C:\\Users\\602836\\Downloads\\iperf-2.0.5-win32',save_path='C:\\Project_TV\\device_02\\files_data\\')
# print(iperf2)