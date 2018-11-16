# encoding='utf-8'
import time
from multiprocessing import Process

from haf.bench import HttpApiBench
from haf.busclient import BusClient
from haf.case import HttpApiCase
from haf.log import Log

logger = Log.getLogger(__name__)

class Loader(Process):
    def __init__(self):
        super().__init__()
        self.bus_client = None
        self.daemon = True

    def run(self):
        self.bus_client = BusClient()
        logger.debug("start loader {} ".format(self.pid))
        while True:
            benchs = self.bus_client.get_bench()
            print(benchs)
            benchs.set("test", HttpApiBench())
            params_queue = self.bus_client.get_param()
            if not params_queue.empty() :
                param = params_queue.get()
                logger.debug("loader {} -- {}".format(self.pid, param))
                while True:
                    case_queue = self.bus_client.get_case()
                    case = HttpApiCase()
                    case_queue.put(case)
                    time.sleep(1)
                break

            time.sleep(3)