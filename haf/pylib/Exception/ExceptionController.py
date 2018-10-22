
'''
# define Exceptions here
'''

import os, sys, time, datetime, json

class ExceptionBase(Exception):
    def __init__(self, ExceptionInfo=""):
        Exception.__init__(self)
        self.ExceptionInfo = ExceptionInfo

    def __str__(self):
        return "Exception"
    
    def getInfo(self):
        return self.__str__() + "--" + self.ExceptionInfo

class NetworkExceptionBase(ExceptionBase):
    def __init__(self, ExceptionInfo=""):
        ExceptionBase.__init__(self, ExceptionInfo)
    
    def __str__(self):
        return "NetworkExceptionBase"

    def getInfo(self):
        return self.__str__() + "--" + self.ExceptionInfo


class NetworkUnavaliableException(NetworkExceptionBase):
    def __init__(self, ExceptionInfo=""):
        NetworkExceptionBase.__init__(self, ExceptionInfo)

    def __str__(self):
        return "NetworkUnavaliableException"
    
    def getInfo(self):
        return self.__str__() + "--" + self.ExceptionInfo

class NetworkIPIllegalException(NetworkExceptionBase):
    def __init__(self, ExceptionInfo=""):
        NetworkExceptionBase.__init__(self, ExceptionInfo)

    def __str__(self):
        return "NetworkIPIllegalException"
    
    def getInfo(self):
        return self.__str__() + "--" + self.ExceptionInfo


class NoneTypeException(ExceptionBase):
    def __init__(self, ExceptionInfo=""):
        ExceptionBase.__init__(self, ExceptionInfo)

    def __str__(self):
        return "NoneTypeException"

    def getInfo(self):
        return self.__str__() + "--" + self.ExceptionInfo



    
