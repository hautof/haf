# -*- encoding:utf-8 -*-

'''
file name : log
description : the log of all process need
others:
    usage:
        logger = Log.getLogger(__name__)
        # in multi-process
        logger.bind_busclient(bus_client)
        logger.bind_process(pid)
        # if no output
        logger.set_output(False, nout)
        # if local logger
        logger.set_output(True, nout)
        logger.debug(msg, logger_name)
        logger.info
        logger.warning
        logger.error
'''


import logging, os, time
from haf.busclient import BusClient
from haf.common.sigleton import SingletonType


class BaseLogger(metaclass=SingletonType):
    '''
    BaseLogger
    SingletonType class
    '''

    def __init__(self, logger_name):
        self.logger_name = logger_name
        self.bus_client = None
        self.process_id = 0
    
    # here using this function to reconnect to the bus : loader, runner, recorder
    def bind_busclient(self, bus_client: BusClient):
        self.bus_client = BusClient(bus_client.domain, bus_client.port, bus_client.auth_key)
        self.log = self.bus_client.get_log()

    # bind the pid of the process
    def bind_process(self, process_id):
        self.process_id = process_id

    # set out put or not, or using local logger
    def set_output(self, local_logger, nout=True, debug=False):
        self.local_logger = local_logger
        self.nout = nout
        self.debug_ = debug

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

    def log_output(self, msg, origin_msg):
        '''
        print msg with params nout
        :param msg:
        :return: None
        '''
        if not self.nout:
            if origin_msg.get('level')=='debug' and not self.debug_:
                return
            print(msg)

    def write_local_logger(self, msg):
        '''
        write the log with local writer
        :param msg:
        :return:
        '''
        msg_now = f"{self.now} {msg.get('level')} <{msg.get('process')}> [{msg.get('logger_name')}] {msg.get('msg')}"
        self.log_output(msg_now, msg)
        dir = f"./data/log/"
        if not os.path.exists(dir):
            try:
                os.makedirs(dir)
            except Exception as error:
                pass
        full_name = f"{dir}/log.log"
        try:
            with open(full_name, 'a+') as f:
                f.write(f"{msg_now}\n")
                f.close()
        except Exception as e:
            with open(full_name, 'a+', encoding='utf-8') as f:
                f.write(f"{msg_now}\n")
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
        '''
        write to local or not
        :param msg:
        :return:
        '''
        if self.bus_client is None:
            self.bus_client = BusClient()
        if self.local_logger:
            self.write_local_logger(msg)
        else:
            if msg.get('level')=='debug' and not self.debug_:
                return 
            self.log.put(msg)


class Log:
    @staticmethod
    def getLogger(logger_name):
        logger = BaseLogger(logger_name)
        return logger

