# encoding='utf-8'
import os
import time, logging
from multiprocessing import Process
from haf.busclient import BusClient
from haf.config import *
from haf.common.log import Log

logger = Log.getLogger(__name__)


class Logger(Process):
    def __init__(self, case_name, log_dir, bus_client: BusClient):
        super().__init__()
        self.daemon = True
        self.bus_client = bus_client
        self.case_name = case_name
        self.log_dir = log_dir
        self.loggers = {}

    def run(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s <%(process)d> [%(name)s] %(message)s')
        logger.bind_busclient(self.bus_client)
        logger.info("start system logger")
        log_home = f"{self.log_dir}/{self.case_name}"
        if not os.path.exists(log_home):
            os.makedirs(log_home)
        # here delete BusClient(), using input bus_client
        # self.bus_client = BusClient()
        try:
            log_queue = self.bus_client.get_log()
            while True:
                if log_queue.empty():
                    time.sleep(0.01)
                    continue
                log = log_queue.get()
                self.log_handler(log)
        except KeyboardInterrupt as key_e:
            print(BANNER_STRS_EXIT)

    def split_log(self, log):
        try:
            return log.rsplit("$%", 2)
        except Exception as ee:
            return f"log$%error$%{log}"

    def log_print(self, log):
        logger_name = log.get("logger_name")
        level = log.get("level")
        msg = log.get("msg")
        if logger_name not in self.loggers:
            self.loggers[logger_name] = logging.getLogger(logger_name)

        logger = self.loggers.get(logger_name)
        if level=="debug":
            logger.debug(msg)
        elif level=="info":
            logger.info(msg)
        elif level=="wraning":
            logger.warning(f"\33[33m{msg}\33[0m")
        elif level=="error":
            logger.error(f"\33[31m >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> \33[0m")
            logger.error(f"\33[31m | {msg}\33[0m")
            logger.error(f"\33[31m <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< \33[0m")
        elif level=="critical":
            logger.critical(f"\33[5m{msg}\33[0m")

    def log_handler(self, log):
        self.log_print(log)
        log = log.get("msg")
        try:
            temp1, temp2, msg = self.split_log(log)
        except :
            temp1 = "error"
            temp2 = "error"
            msg = log

        if "loader" in temp2:
            self.loader_handler(temp1, msg)
        elif "runner" in temp2:
            self.runner_handler(temp1, msg)
        elif "recorder" in temp2:
            self.recorder_handler(temp1, msg)
        elif "system" in temp2:
            self.system_handler(temp1, temp2, msg)
        elif "error" in temp2:
            self.error_handler(temp1, msg)
        else:
            self.case_handler(temp1, temp2, msg)

    def loader_handler(self,temp1, msg):
        self.write("loader", temp1, msg)

    def runner_handler(self, temp1, msg):
        self.write("runner", temp1, msg)

    def case_handler(self, temp1, temp2, msg):
        self.write(temp1, temp2, msg)

    def recorder_handler(self, temp1, msg):
        self.write("recorder", temp1, msg)

    def system_handler(self, temp1, temp2, msg):
        self.write("system", f"{temp1}.{temp2}", msg)

    def error_handler(self, temp1, msg):
        self.write("error", temp1, msg)

    def write(self, dir, filename, msg):
        dir = f"{self.log_dir}/{self.case_name}/{dir}"
        if not os.path.exists(dir):
            os.makedirs(dir)
        full_name = f"{dir}/{filename}.log"
        with open(full_name, 'a+') as f:
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

    def end_handler(self):
        result_handler = self.bus_client.get_result()
        result_handler.put(SIGNAL_RESULT_END)
        case_handler = self.bus_client.get_case()
        case_handler.put(SIGNAL_CASE_END)

