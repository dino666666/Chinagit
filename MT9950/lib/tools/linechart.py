#_*_encoding:GBK*_
import csv,cv2
import matplotlib.pyplot as plt
def line_chart(num,csv_path,picture_path,unit=[]):
    if num>6:
        print('暂时设定上限为6张图(需要可增加）')
        return False
    op=open(csv_path,'r')
    csv_read=csv.reader(op)
    createVar = locals()
    listTemp = range(0, num)
    for i, s in enumerate(listTemp):
        # print(i)
        createVar['x' + str(i)] = []
        createVar['y' + str(i)] = []
    flag=0
    line=0
    for row in csv_read:
        line+=1
        if flag==0:
            title_list=row
            flag=1
        number = 0
        for i in row:
            try:
                if number==0:
                    for j in range(0,num):
                        createVar['x' + str(j)].append(float(i))
                        # print('x' + str(j))
                        # print(createVar['x' + str(j)])
                if number!=0:
                    createVar['y' + str(number-1)].append(float(i))
                    # print('y'+str(number-temp))
                    # print(createVar['y' + str(number-temp)])
                number+=1
            except:
                None
        # print(row)
    length=line//500
    # print(length)
    if length==0:
        plt.figure(figsize=(16, num*3))
    else:
        plt.figure(figsize=(16*length, num*3))
    for i in range(0,num):
        title = 0
        label=0
        plt.subplot(num, 1, i+1)
        # print(createVar['x' + str(i)])
        # print(createVar['y' + str(i)])
        plt.plot(createVar['x' + str(i)], createVar['y' + str(i)], label='weight changes', linewidth=0.3, color='r')
        for j in title_list:
            if title==i+1:
                plt.title(j)
            title+=1
        for l in unit:
            if label==i:
                plt.ylabel(l)
            label+=1
    # plt.show()
    plt.margins(x=0)
    plt.savefig(picture_path)

# line_chart(temp,unit=['R','G','B'],csv_path='/home/oneplus/Python-DATA/video1.csv',picture_path='/home/oneplus/Python-DATA/video1.png')

# cv2.imshow('dd','/home/oneplus/Python-DATA/video17.png')


