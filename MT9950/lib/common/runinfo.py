#_*_encoding:GBK_*_
import logging,os,time
class run_log(object):
    def __init__(self,logger,logging_path):
        self.logger=logging.getLogger(logger)
        self.logging_path=logging_path
        self.logger.setLevel(logging.INFO)
        lt=time.strftime('%Y%m%d%H',time.localtime(time.time()))
        logpath=self.logging_path+'/run'+lt+'.log'
        fileh=logging.FileHandler(logpath)
        fileh.setLevel(logging.INFO)
        consoleh=logging.StreamHandler()
        consoleh.setLevel(logging.INFO)
        fromatter=logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
        fileh.setFormatter(fromatter)
        consoleh.setFormatter(fromatter)
        self.logger.addHandler(fileh)
        self.logger.addHandler(consoleh)
    def getlog(self):
        return self.logger
# log=log('log').getlog()
# log.info('aa')