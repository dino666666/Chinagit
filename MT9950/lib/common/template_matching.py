#_*_encoding:GBK_*_
from skimage.measure import compare_ssim
import imutils,cv2
def compare(picture1,picture2,value=1):
    imageA = cv2.imread(picture1)
    imageB = cv2.imread(picture2)

    # imageA = cv2.resize(image1, (1080,720), interpolation=cv2.INTER_CUBIC)
    # imageB = cv2.resize(image2, (1080,720), interpolation=cv2.INTER_CUBIC)

    grayA = cv2.cvtColor(imageA,cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB,cv2.COLOR_BGR2GRAY)

    (score,diff) = compare_ssim(grayA,grayB,full = True)
    diff = (diff*255).astype("uint8")
    print("SSIM:{}".format(score))
    thresh = cv2.threshold(diff,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        # print(c)
        (x,y,w,h) = cv2.boundingRect(c)
        cv2.rectangle(imageA,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.rectangle(imageB,(x,y),(x+w,y+h),(0,0,255),2)
    if float(score) >= float(value):
        # print(float(score))
        return True
    else:
        cv2.imwrite(picture2, imageB)
        return False
