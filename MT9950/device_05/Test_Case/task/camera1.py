#_*_encoding:GBK*_
import cv2,time,numpy as np,logging
from lib.common.bright import brightness
logging.basicConfig(level=logging.DEBUG,format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')

# !/usr/bin/python3
import cv2

## opening videocapture
cap = cv2.VideoCapture(2)

## some videowriter props
sz = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
      int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
ret, frame = cap.read()
path = '/home/oneplus/Python-Pictures/temp/'
while ret:
    T = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    name = path + T + '.jpg'
    cv2.imwrite(name,frame)
    time.sleep(15)
    ret, frame = cap.read()

cap.release()