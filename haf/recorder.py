# encoding='utf-8'
import time
from multiprocessing import Process

from haf.busclient import BusClient
from haf.case import HttpApiCase
from haf.common.exception import FailRecorderException
from haf.common.log import Log
from haf.result import HttpApiResult
from haf.config import *

logger = Log.getLogger(__name__)


class Recorder(Process):
    def __init__(self):
        super().__init__()
        self.bus_client = None
        self.daemon = True
        self.results = []

    def run(self):
        try:
            logger.info("start recorder {} ".format(self.pid))
            self.bus_client = BusClient()
            while True:
                results = self.bus_client.get_result()
                if not results.empty() :
                    result = results.get()
                    if isinstance(result, HttpApiResult):
                        if isinstance(result.case, HttpApiCase):
                            logger.info("recorder {} -- {}.{}.{} is {}".format(self.pid, result.case.ids.id, result.case.ids.subid, result.case.ids.name, result.result))
                        else:
                            logger.info("recorder {} == wrong result!")
                        self.result_handler(result)
                    elif result == SIGNAL_RESULT_END:
                        self.end_handler()
                        break
                time.sleep(0.1)
        except Exception:
            raise FailRecorderException

    def end_handler(self):
        logger.info("end recorder {} ".format(self.pid))
        system_handler = self.bus_client.get_system()
        system_handler.put(SIGNAL_RECORD_END)

    def result_handler(self, result):
        self.results.append(result)
        logger.info("from {} to {}, result is {}".format(result.begin_time, result.end_time, result.result))