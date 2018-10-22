#encoding='utf-8'


import os, sys, platform
sys.path.append("..")

from haf.pylib.Log.LogController import LogController

class_name = "PlatformTool"
class PlatformTool(object):
    '''
    与系统类型相关的 工具
    '''
    def __init__(self):
        pass

    @staticmethod
    def getPlatformIsWindows():
        '''
        判断 平台是否为 Windows

        :return: bool
        '''
        if platform.system() == "Windows":
            return True
        return False
    
    @staticmethod
    def getPlatformIsLinux():
        return not PlatformTool.getPlatformIsWindows()