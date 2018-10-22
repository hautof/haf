'''
# FTP.py
# using to connect ftp file
# functinos:
    1, connect
    2, close
    3, get file from ftp
    4, put file to remote
'''

import os, sys, datetime, time
from ftplib import FTP
from haf.pylib.Log.LogController import LogController
from haf.pylib.Check.CheckIP import CheckIP

class FtpTool(object):
    
    def __init__(self, ip, port=21, bufsize=1024, username=None, password=None):
        self.class_name = "Ftp"
        self.ls = LogController.getLogger(self.class_name)
        if not CheckIP.checkIP(ip):
            self.ls.log_print('warn', ip + ' is not valuable !')
        
        self.ip = ip
        
        if username is not None:
            self.username = username
        else:
            self.username = 'anynomous'
        
        if password is not None:
            self.password = password
        else:
            self.password = None

        self.port = port
        self.bufsize = bufsize

        if not hasattr(self,'ftp'):
            self.ftp = FTP()
        self.Connect()
        
        

    def __str__(self):
        return self.class_name

    def Connect(self):
        try:
            self.ftp.connect(self.ip, self.port)
            self.ftp.login(self.username, self.password)
        except Exception as e:
            self.ls.log_print('error', str(e))

    def getFile(self, remote, local):
        try:
            fp = open(local, 'wb')
            self.ftp.retrbinary('RETR' + remote, fp.write, self.bufsize)
            self.ftp.set_debuglevel(0)
            fp.close()
        except Exception as e:
            self.ls.log_print('error', str(e))

    def putFile(self, local, remote):
        try:
            fp = open(local, 'rb')
            self.ftp.storbinary('STOR'+remote, fp, self.bufsize)
            self.ftp.set_debuglevel(0)
            fp.close()
        except Exception as e:
            self.ls.log_print('error',str(e))
        
    def Close(self):
        if self.ftp is not None:
            self.ftp.close()