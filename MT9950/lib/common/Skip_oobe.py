import time

from lib.common.adbevent import adb

class Skip(object):
    def __init__(self,device):
        self.device = device
        self.adb = adb(self.device)


    def skip_oobe(self):

        self.adb.ok(1,40)
        self.adb.ok(1,2)
        self.adb.ok(1, 2)
        self.adb.down(30, 1)
        self.adb.ok(1, 1)
        self.adb.ok(1, 40)
        self.adb.ok(1, 1)
        self.adb.ok(1, 1)

    def skip_sleep(self):
        self.adb.order(" monkey -p com.android.tv.settings 1")
        time.sleep(1)
        self.adb.down(6, 1)
        self.adb.ok(1, 1)
        self.adb.down(2, 1)
        self.adb.ok(1, 1)
        self.adb.ok(1, 1)
        self.adb.back(1, 1)
        self.adb.down(1, 1)
        self.adb.left(3, 1)
        self.adb.back(2, 1)
#
# Skip("0000a091a2009e05").skip_oobe()
# Skip("0000a091a2009e05").skip_sleep()