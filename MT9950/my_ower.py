
#_*_encoding:GBK*_
import cv2 as cv,os,time
import numpy as np

def template_part(picture1,picture2,num=0.85,type=0):
    tpl =cv.imread(picture1)
    target = cv.imread(picture2)
    th, tw = tpl.shape[:2]
    result = cv.matchTemplate(target, tpl, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    # print(min_val,'min_val')
    # print(max_val,'max_val')
    # print(min_loc,'min_loc')
    # print(max_loc,'max_loc')
    # print('over')
    tl = max_loc
    # print(tl,'tl')
    br = (tl[0]+tw, tl[1]+th)   #br是矩形右下角的点的坐标
    # print(br,'br')
    # print('over')
    cv.rectangle(target, tl, br, (0, 0, 255), 2)
    print(float(max_val))

    if float(max_val) > num:
        if type == 0:
            os.remove(picture2)

        return True,br
    else:
        result = picture2
        cv.imwrite(result, target)
        return False,br

picture1 = "/home/oneplus/IndiaData/device/picture/Sleep20200730141220.png"
picture2 = "/home/oneplus/IndiaData/device/picture/Setting.png"
picture3 = "/home/oneplus/IndiaData/device/picture/Sleep20200730131037.png"

template_part(picture1,picture2)
template_part(picture3,picture2)

























