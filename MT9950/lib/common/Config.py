#_*_encoding:utf-8_*_
import configparser,os
def Config(name):
    #用来获得config.ini的值
    cf=configparser.ConfigParser()
    cfpath='C:\Project\Config\config.ini'
    cf.read(cfpath)
    read=cf.get('APP',name)
    return read