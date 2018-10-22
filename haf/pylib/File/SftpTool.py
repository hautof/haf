'''
# Sftp.py
# using to connect to remote sftp server
# functions:
    1, connect to remote sftp server
    2, put file from local to remote
    3, get file from remote
    4, close connection
# author : wei.meng @20180411
# version : 0.0.1
'''

import paramiko
import sys
import time

from haf.pylib.Log.LogController import LogController
from haf.pylib.Check.CheckIP import CheckIP


class SftpTool(object):
    def __init__(self,ipadd, username, password):

        self.class_name = "SftpTool" 
        self.ls = LogController.getLogger(self.class_name)
        
        if isinstance(ipadd, str):            
            self.ip = ipadd       
        else:
            self.ip = str(ipadd)
        if not Check.checkIP(self.ip):
            self.ls.log_print('warn', self.ip + 'is not the valuable ip!', '__init__')

        if isinstance(username, str):
            self.username = username
        else:
            self.username = str(username)
        if isinstance(password, str):
            self.password = password
        else:
            self.username = str(password)
        
        self.Connect()

    def __str__(self):
        return self.class_name

    def Connect(self):
        try:
            if not hasattr(self, "sftp"):
                self.ls.log_print("system", "connect to  " + str(self.ip), self.Connect.__name__)
                self.sftp = paramiko.Transport(self.ip,22)
                self.sftp.connect(username=self.username,password=self.password)
                self.sf = paramiko.SFTPClient.from_transport(self.sftp)
        except Exception as e:
            self.ls.log_print("system", "wrong with it -- " + str(e), self.Connect.__name__)

    def PutFile(self, localfile, remotefile):
        try:
            self.ls.log_print("system",str(localfile) + " ====> " + str(remotefile), self.PutFile.__name__)
            self.sf.put(localfile,remotefile)
            self.ls.log_print("system","success", self.PutFile.__name__)
        except Exception as e:
            self.ls.log_print("system","wrong with it -- " + str(e), self.PutFile.__name__)

    def GetFile(self, remotefile, localfile):
        try:
            self.ls.log_print("system",str(localfile) + " <==== " + str(remotefile), self.GetFile.__name__)
            self.sf.get(remotefile,localfile)                                                                                                               
            self.ls.log_print("system", "success")
        except Exception as e:
            self.ls.log_print("system", "wrong with -- " + str(e), self.GetFile.__name__)
    
    def OpenFile(self, remotefile, mode='r'):
        try:
            f = self.sf.open(remotefile, mode)
            allcontent = f.readlines()
            f.close()
            return allcontent
        except Exception as e:
            self.ls.log_print('error', 'wrong with -- ' + str(e), self.OpenFile.__name__)

    def Close(self):
        self.sftp.close()


