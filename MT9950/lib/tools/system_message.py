# encoding:GBK*_
import os

device = '001AAAAJC10018FA05'
a = os.popen('adb -s ' + device + ' shell top -d 5')
read = a.readline()

while read:
    info = read.split(' ')
    mem = 0
    mem_list = []
    for i in info:
        # print(i)
        if '%cpu' in i:
            total_cpu = i.split('%')[0]
            # print(i)
            # print(total_cpu)

        if 'idle' in i:
            # print(i)
            idle_cpu = i.split('%')[0]
            # print(idle_cpu)

            try:
                use = int(total_cpu) - int(idle_cpu)
                print('当前CPU使用率:',use,'%')
            except:
                pass

        if 'Mem' in i:
            # print(read)
            # print(info)
            mem = 1

        if mem == 1:
            if 'k' in i:
                # print(i)
                mem_list.append(i.split('k')[0])
                # print(mem_list)
                try:
                    buffers_mem = (int(mem_list[3])/int(mem_list[0])) * 100
                    use_men = (int(mem_list[1])/int(mem_list[0])) * 100
                    print('当前内存使用率',use_men,"%")
                    print('当前缓冲内存占据：',buffers_mem,'%')
                except:
                    pass

    read = a.readline()