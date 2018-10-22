#encoding='utf-8'

import os, sys
from haf.pylib.Log.LogController import LogController
from haf.pylib.tools.PlatformTool import PlatformTool

class_name = "FileCopy"
logger = LogController.getLogger(class_name)

class FileCopy(object):
    def __init__(self):
        pass

    @staticmethod
    def copy(source, dist):
        logger.log_print("info", "copy " + source + " to " + dist)
        if PlatformTool.getPlatformIsLinux():
            os.system("cp -rf " + source + "/* " + dist + "/")
        else:
            source = source.replace("/", "\\")
            dist = dist.replace("/", "\\")
            command = "echo D | xcopy /s /h " + source + " " + dist + "\\"
            os.system(command)