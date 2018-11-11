#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
author : wei.meng
date : 20180730
version : 1.0
'''
import sys, os, time

from haf.pylib.NetWork.NetWorkController import NetWorkController
from haf.pylib.Log.LogController import LogController

class FileGet(object):
    '''
    获取文件 管理类
    '''
    def __init__(self):
        self.ls = LogController.getLogger("FileGet")
        self.ls.log_print ("system", "[getfiles]------------")

    def GetFile(self, protocol:str, remote:str, local:str, *args):
        if protocol == "default":
            self.getfile_windows_copy(remote, local)
        elif protocol == "ftp":
            self.getfile_ftp(remote, local, *args);
        
    def getfile_windows_copy(self,remote:str,local:str):
        self.ls.log_print ("system", "[getfile] remote: " + str(remote))
        self.ls.log_print ("system", "[getfile] local : " + str(local))
        copycmd = "xcopy /yse %s  %s\\ "%(remote,local)
        self.ls.log_print ("system", "[getfile] cmd= " + str(copycmd))
        if os.system(copycmd) == 0 :
            self.ls.log_print ("system", "[getfile] copy ok")
        else:
            self.ls.log_print ("system", "[getfile] copy fail")
            exit(1)

    def Getfile_filename(self,remote:str,local:str,filename:str):
        self.ls.log_print ("system", "[getfile] remote: " + str(remote + "\\" + filename))
        self.ls.log_print ("system", "[getfile] local : " + str(local + "\\" + filename))
        copycmd = "echo F | xcopy /yse %s  %s "%(remote +"\\" + filename,local +"\\" + filename)
        self.ls.log_print ("system", "[getfile] cmd= " + str(copycmd))
        if os.system(copycmd) == 0 :
            self.ls.log_print ("system", "[getfile] copy ok")
        else:
            self.ls.log_print ("system", "[getfile] copy fail")


    def Getfile_1(self,remote:str,local:str):
        self.ls.log_print ("system", "[getfile] remote: " + str(remote))
        self.ls.log_print ("system", "[getfile] local : " + str(local))
        copycmd = "echo F | xcopy /yse %s  %s "%(remote,local)
        self.ls.log_print ("system", "[getfile] cmd= " + str(copycmd))
        if os.system(copycmd) == 0 :
            self.ls.log_print ("system", "[getfile] copy ok")
        else:
            self.ls.log_print ("system", "[getfile] copy fail")

    def getfile_ftp(self,remote:str,local:str, *args):
        self.ls.log_print ("system", "[getfile_ftp] remote : " + str(remote))
        self.ls.log_print ("system", "[getfile_ftp] local  : " + str(local))
        if len(args) > 2:
            nwc = NetWorkController()
            ftp = nwc.getProtocol("ftp", *args)
            ftp.Connect()


            
'''
    def GetSCPfile(self, remote,local,ip):
        self.ls.log_print ("system", "[getscpfile] remote : " + str(remote))
        self.ls.log_print ("system", "[getscpfile] local  : " + str(local))
        sftp = SftpTool(ip)
        sftp.Connect()
        sftp.GetFile(remote, local)
        sftp.Close()
'''
        
if __name__=="__main__":
    fg = FileGet()
    fg.GetFile("ftp","", "","192.168.41.208","root","testzhan123")



