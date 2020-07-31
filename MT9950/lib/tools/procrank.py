#_*_encoding:GBK*_
import os
class procrank(object):
    def __init__(self,device):
        self.device = device
    def Rss(self,apkpage):
        RssValue = 0
        command = 'adb -s ' + self.device + ' shell "procrank | grep -i ' + apkpage + '"'
        getRss = os.popen(command)
        readRss = getRss.readline()
        while readRss:
            if apkpage in readRss:
                print(readRss)
                Rss = readRss.split(' ')
                print(Rss)
                while '' in Rss:
                    Rss.remove('')
                RssValue = Rss[2].split('K')[0]
                print(RssValue)
            readRss = getRss.readline()
        return RssValue
# procrank = procrank(device_05='0000040000000008')
#
# getRss = procrank.Rss('com.google.android.youtube.tv')
#
# print(getRss)