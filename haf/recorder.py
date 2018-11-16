# encoding='utf-8'
import time
from multiprocessing import Process

from haf.busclient import BusClient
from haf.log import Log
from haf.result import HttpApiResult
from haf.config import *

logger = Log.getLogger(__name__)

class Recorder(Process):
    def __init__(self):
        super().__init__()
        self.bus_client = None
        self.daemon = True

    def run(self):
        logger.debug("start recorder {} ".format(self.pid))
        self.bus_client = BusClient()
        while True:
            results = self.bus_client.get_result()
            if not results.empty() :
                result = results.get()
                if isinstance(result, HttpApiResult):
                    logger.debug("recorder {} -- {}".format(self.pid, result))
                elif result == SIGNAL_RESULT_END:
                    self.end_handler()
                    break
            time.sleep(0.1)

    def end_handler(self):
        logger.debug("end recorder {} ".format(self.pid))
        system_handler = self.bus_client.get_system()
        system_handler.put(SIGNAL_RECORD_END)
