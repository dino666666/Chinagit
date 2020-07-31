#_*_encoding:GBK*_
import cv2,time,numpy as np,logging
from lib.common.bright import brightness
logging.basicConfig(level=logging.DEBUG,format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

import cv2

def picture(path,camera_number=0,num=1,times=2,mode='p'):
    ## opening videocapture
    cap = cv2.VideoCapture(camera_number)

    ## some videowriter props
    # sz = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
    #       int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    path = path

    for i in range(num):
        ret, frame = cap.read()
        T = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        name = path + mode + T + '.jpg'
        cv2.imwrite(name,frame)
        time.sleep(times)

    cap.release()
    return name
# for i in range(10):
#     picture(path='/home/oneplus/IndiaData/log/')
#     time.sleep(10)