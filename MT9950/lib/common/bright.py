#_*_encoding:GBK_*_
import math
from PIL import Image
from PIL import ImageStat
def brightness(im_file,type=0):
    if type==0:
        print(im_file)
        im = Image.open(im_file)
    else:
        im = Image.fromarray(im_file)
    stat = ImageStat.Stat(im)
    r,g,b = stat.mean
    return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))
# print(brightness('C:\\picture\\20191009192150.jpg'))