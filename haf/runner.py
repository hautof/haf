# encoding='utf-8'
import time
from multiprocessing import Process

from haf.busclient import BusClient
from haf.case import HttpApiCase
from haf.result import HttpApiResult
from haf.log import Log

logger = Log.getLogger(__name__)

class Runner(Process):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.bus_client = None

    def load(self):
        pass

    def run(self):
        self.bus_client = BusClient()
        while True:
            case_handler = self.bus_client.get_case()
            if not case_handler.empty() :
                case = case_handler.get()
                logger.debug("runner {} -- {}".format(self.pid, case))
                result = self.bus_client.get_result()
                result.put(HttpApiResult())
            time.sleep(1)