import os, sys, time

from haf.pylib.Log.LogController import LogController


class SQLConfig(object):
    '''
    sql config 实体
    '''
    def __init__(self):
        self.class_name = "SQLConfig"
        self.logger = LogController.getLogger(self.class_name)
        self.host = None
        self.port = None
        self.username = None
        self.password = None
        self.database= None
        self.protocol = None
        self.id = None
        self.sqlname = None
    
    def constructor(self, *args):
        '''
        构造器
        '''
        self.logger.log_print("info", "start", "constructor ")
        if len(args) > 0:
            if isinstance(args[0], dict):
                self.logger.log_print("info", str(args[0].get("host")), "constructor ")
                config = args[0]
                self.host = str(config.get("host"))
                self.port = config.get("port")
                self.username = str(config.get("username"))
                self.password = str(config.get("password"))
                self.database= str(config.get("database"))
                self.protocol = str(config.get("protocol"))
                self.id = config.get("id")
                self.sqlname = str(config.get("sql_name"))
        self.logger.log_print("info", "ok", "constructor ")
        
