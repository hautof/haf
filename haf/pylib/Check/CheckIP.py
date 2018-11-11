'''
# Check.py
# using to check all things
# functions:
    1, check ip is ok
# modify : python3 the subprocess.popen return the list not str
'''

import re
import os, sys, time, datetime, json, subprocess
from haf.pylib.Exception.ExceptionController import * 

class CheckIP(object):

    def __init__(self):
        self.class_name = 'Check'
    
    def __str__(self):
        return self.class_name

    @staticmethod
    def checkIP(ipadd:str):
        if isinstance(ipadd, str):
            ip = ipadd
        else:
            ip = str(ipadd)

        if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip):
            return True
        else:
            raise NetworkIPIllegalException(ipadd + " is illegal!")
        
    @staticmethod
    def run_cmd(cmd:str):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = "\n".join(str(s) for s in p.stdout.readlines() if s not in [None])
        retval = p.wait()
        if not "TTL" in output:
            return False
        return True

    @staticmethod
    def PingIP(ipadd:str):
        if Check.checkIP(ipadd):
            check_ping = False
            temp_int = 1
            while temp_int < 3 and not check_ping:
                try:

                    if not check_ping:
                        if Check.run_cmd("ping " + str(ipadd)):
                            check_ping = True
                        else:
                            check_ping = False
                except:
                    time.sleep(1)
                    temp_int += 1
                    continue
            if check_ping:
                return True
            else:
                raise NetworkUnavaliableException
            
    @staticmethod
    def checkNoneType(cla):
        if cla is None:
            raise NoneTypeException

if __name__ == '__main__':
    check = Check()
    print (check.checkIP('11.16.130.129'))
    print (check.run_cmd('ping 10.16.129.27'))