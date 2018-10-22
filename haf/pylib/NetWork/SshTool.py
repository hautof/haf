#-*- coding: utf-8 -*-
#!/usr/bin/python 

'''
# SSH.py
# using to ssh connect to remote and execute some commands
# functions:
    1, connect to ssh server
    2, Execute command
    3, Execute System command
    4, Execute no return command
    5, close the connection
# old...
# version : 1.4
# attention ：using paramiko module --- using 'pip install paramiko' to install the module
# functon : ssh and sftp function
# author : mengwei
# date : 20180730
# modify : -add Sftp module to transport the file
'''

import paramiko
import sys
import time
from haf.pylib.Log.LogController import LogController

class SshTool(object):

    def __init__(self,ipadd,username,password):
        self.class_name = "SshTool"

        if isinstance(ipadd, str):            
            self.ip = ipadd       
        else:
            self.ip = str(ipadd)
        if isinstance(username, str):
            self.username = username
        else:
            self.username = str(username)
        if isinstance(password, str):
            self.password = password
        else:
            self.username = str(password)

        self.ls = LogController.getLogger(self.class_name)
        self.Connect()
    
    def __str__(self):
        return self.class_name

    def Connect(self):
        try:
            if not hasattr(self, "connect"):
                self.connect = paramiko.SSHClient()
                self.connect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.connect.connect(self.ip,22,self.username,self.password,timeout=5)
                
        except Exception as e:
            self.ls.log_print("system","wrong with it -- " + str(e), self.Connect.__name__)

    def Exec(self,cmd):
        try:
            self.ls.log_print("system", str(cmd), self.Exec.__name__)
            stdin, stdout, stderr = self.connect.exec_command(cmd)
            out = stdout.readlines()
            return out
        except Exception as e:
            self.ls.log_print("system", "wrong with it -- " + str(e), self.Exec.__name__)
            
    def Exec_system(self, cmd):
        try:
            stdin, stdout, stderr = self.connect.exec_command(cmd)
            out = stdout.readlines()
            return out
        except Exception as e:
            self.ls.log_print("error", "error is --- " + str(e), self.Exec_system.__name__)

    def Exec_noreturn(self,cmd):
        try:
            self.ls.log_print("system", str(cmd), self.Exec_noreturn.__name__)
            stdin, stdout, stderr = self.connect.exec_command(cmd)
        except Exception as e:
            self.ls.log_print("system", "wrong with it -- " + str(e), self.Exec_noreturn.__name__)
    
    def Close(self):
        try:
            self.connect.close()
        except Exception as e:
            self.ls.log_print("system", "wrong with it -- " + str(e), self.Close.__name__)



# sample to show how ssh use
if __name__ == "__main__":
    ssh = Ssh("192.168.11.1","root","slamware123")
    ssh.Connect()
    ssh.Exec("mv /etc/sdp_ref.json /home/root/sdp_ref.json ")
    ssh.Exec("mv /home/root/sdp_ref_simulator.json /etc/sdp_ref.json ")
    ssh.Exec("reboot -n")            
    ssh.Close()