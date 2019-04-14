# -*- encoding:utf-8 -*-

import logging, os, time
from haf.busclient import BusClient
from haf.common.sigleton import SingletonType


class BaseLogger(metaclass=SingletonType):

    def __init__(self, logger_name):
        self.logger_name = logger_name
        self.bus_client = None
        self.process_id = 0
    
    # here using this function to reconnect to the bus : loader, runner, recorder
    def bind_busclient(self, bus_client: BusClient):
        self.bus_client = BusClient(bus_client.domain, bus_client.port, bus_client.auth_key)
    
    def bind_process(self, process_id):
        self.process_id = process_id

    def set_output(self, local_logger):
        self.local_logger = local_logger

    def debug(self, msg, logger_name=None):
        msg = {"process": self.process_id, "logger_name":self.logger_name if not logger_name else logger_name, "level":"debug", "msg": msg}
        self.msg_write(msg)

    def info(self, msg, logger_name=None):
        msg = {"process": self.process_id, "logger_name":self.logger_name if not logger_name else logger_name, "level":"info", "msg": msg}
        self.msg_write(msg)

    def warning(self, msg, logger_name=None):
        msg = {"process": self.process_id, "logger_name":self.logger_name if not logger_name else logger_name, "level":"warning", "msg": msg}
        self.msg_write(msg)

    def error(self, msg, logger_name=None):
        msg = {"process": self.process_id, "logger_name":self.logger_name if not logger_name else logger_name, "level":"error", "msg": msg}
        self.msg_write(msg)

    def critical(self, msg, logger_name=None):
        msg = {"process": self.process_id, "logger_name":self.logger_name if not logger_name else logger_name, "level":"critical", "msg": msg}
        self.msg_write(msg)

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def write_local_logger(self, msg):        
        dir = f"./data/log/"
        if not os.path.exists(dir):
            os.makedirs(dir)
        full_name = f"{dir}/log.log"
        try:
            with open(full_name, 'a+') as f:
                f.write(f"{self.now}{msg}\n")
                f.close()
        except Exception as e:
            with open(full_name, 'a+', encoding='utf-8') as f:
                f.write(f"{self.now}{msg}\n")
                f.close()
    
    @property
    def now(self):
        '''
        get datetime now to str
        :return: time now str
        '''
        current_time = time.time()
        local_time = time.localtime(current_time)
        time_temp = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        secs = (current_time - int(current_time)) * 1000
        timenow = "%s %03d" % (time_temp, secs)
        return timenow

    def msg_write(self, msg):
        if self.bus_client is None:
            self.bus_client = BusClient()
        if self.local_logger:
            self.write_local_logger(msg)
        else:
            self.bus_client.get_log().put(msg)


class Log:
    @staticmethod
    def getLogger(logger_name):
        logger = BaseLogger(logger_name)
        return logger

