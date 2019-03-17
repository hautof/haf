# -*- encoding:utf-8 -*-

import logging
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

    def msg_write(self, msg):
        if self.bus_client is None:
            self.bus_client = BusClient()
        self.bus_client.get_log().put(msg)


class Log:
    @staticmethod
    def getLogger(logger_name):
        logger = BaseLogger(logger_name)
        return logger

