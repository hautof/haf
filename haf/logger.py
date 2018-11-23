# encoding='utf-8'
import os
import time
import traceback
from multiprocessing import Process

from haf.busclient import BusClient

from haf.config import *


class Logger(Process):
    def __init__(self):
        super().__init__()
        self.bus_client = None
        self.daemon = True

    def run(self):
        self.bus_client = BusClient()
        while True:
            try:
                log_queue = self.bus_client.get_log()
                if log_queue.empty():
                    time.sleep(1)
                    continue
                log = log_queue.get()
                #print(log)
                self.log_handler(log)
            except Exception as e:
                traceback.print_exc()

    def log_handler(self, log):
        if "$%loader$%" in log:
            self.loader_handler(log)
        elif "$%runner$%" in log:
            self.runner_handler(log)
        elif "$%recorder$%" in log:
            self.recorder_handler(log)
        elif "$%system$%" in log:
            self.system_handler(log)
        else:
            self.case_handler(log)


    def loader_handler(self, log):
        sid, loader, msg = log.rsplit("$%", 2)
        self.write("loader", sid, log)


    def runner_handler(self, log):
        sid, runner, msg = log.rsplit("$%", 2)
        self.write("runner", sid, log)

    def case_handler(self, log):
        dir, case, msg = log.rsplit("$%", 2)
        self.write(dir, case, log)

    def recorder_handler(self, log):
        sid, recorder, msg = log.rsplit("$%", 2)
        self.write("recorder", sid, log)

    def system_handler(self, log):
        a, b, msg = log.rsplit("$%", 2)
        self.write("system", "{}.{}".format(a, b), log)


    def write(self, dir, filename, msg):
        dir = "{}/{}".format(LOG_PATH_DEFAULT, dir)
        if not os.path.exists(dir):
            os.makedirs(dir)
        full_name = "{}/{}.log".format(dir, filename)
        with open(full_name, 'a+') as f:
            f.write("{}\n".format(msg))
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

