#_*_encoding:GBK*_
import csv,os,time,random
class csv_write(object):
    def __init__(self,path):
        self.path=path
    def open(self,type=0):
        if type==0:
            if os.path.exists(self.path)==True:
                os.remove(self.path)
                time.sleep(1)
        self.op = open(self.path, 'a+')
        self.csv_write = csv.writer(self.op, lineterminator='\n')
    def write(self,li=[]):
        self.csv_write.writerow(li)
    def close(self):
        self.op.close()
#
# cs=csv_write(path='C:\\Project_TV\\device_01\\videos\\temp.csv')
# cs.open()
# x=['number','value1','value2','value3','value3','value3','value3','value3','value3','value3','value3','value3']
# cs.write(x)
# x=[]
# for i in range(0,100):
#     x.append(i)
#     k = random.randint(0, 100)
#     x.append(k)
#     k = random.randint(0, 100)
#     x.append(k)
#     k = random.randint(0, 100)
#     x.append(k)
#     k = random.randint(0, 100)
#     x.append(k)
#     k = random.randint(0, 100)
#     x.append(k)
#     k = random.randint(0, 100)
#     x.append(k)
#     k = random.randint(0, 100)
#     x.append(k)
#     k = random.randint(0, 100)
#     x.append(k)
#     k = random.randint(0, 100)
#     x.append(k)
#     k = random.randint(0, 100)
#     x.append(k)
#     k = random.randint(0, 100)
#     x.append(k)
#     cs.write(x)
#     x=[]
# cs.close()
# time.sleep(100)

