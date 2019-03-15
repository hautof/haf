# -*- encoding:utf-8 -*-

import logging
from haf.busclient import BusClient


class BaseLogger(object):

    def __init__(self, logger_name):
        self.logger_name = logger_name
        self.bus_client = None

    def bind_busclient(self, bus_client: BusClient):
        self.bus_client = BusClient(bus_client.domain, bus_client.port, bus_client.auth_key)

    def debug(self, msg):
        msg = {"logger_name":self.logger_name, "level":"debug", "msg": msg}
        self.msg_write(msg)

    def info(self, msg):
        msg = {"logger_name":self.logger_name, "level":"info", "msg": msg}
        self.msg_write(msg)

    def warning(self, msg):
        msg = {"logger_name":self.logger_name, "level":"warning", "msg": msg}
        self.msg_write(msg)

    def error(self, msg):
        msg = {"logger_name":self.logger_name, "level":"error", "msg": msg}
        self.msg_write(msg)

    def critical(self, msg):
        msg = {"logger_name":self.logger_name, "level":"critical", "msg": msg}
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

