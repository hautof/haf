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
        self.results = {}
        self.recorder_key = ""

    def run(self):
        try:
            self.recorder_key = f"{self.pid}$%recorder$%"
            logger.info(f"{self.recorder_key} start recorder ")
            self.bus_client = BusClient()
            while True:
                results = self.bus_client.get_result()
                if not results.empty() :
                    result = results.get()
                    if isinstance(result, HttpApiResult):
                        if isinstance(result.case, HttpApiCase):
                            logger.info(f"{self.recorder_key} recorder -- {result.case.ids.id}.{result.case.ids.subid}.{result.case.ids.name} is {result.result}")
                        else:
                            logger.info(f"{self.recorder_key} recorder ! wrong result!")
                            logger.info(f"{self.recorder_key} recorder {result.run_error}")
                        self.result_handler(result)
                    elif result == SIGNAL_RESULT_END:
                        self.end_handler()
                        break
                time.sleep(0.1)
        except Exception:
            raise FailRecorderException

    def end_handler(self):
        logger.info(f"{self.recorder_key} end recorder")
        self.json_result_handler()
        system_handler = self.bus_client.get_system()
        system_handler.put(SIGNAL_RECORD_END)

    def result_handler(self, result):
        if self.results.get(result.case.bench_name) is None:
            self.results[result.case.bench_name] = []
        self.results[result.case.bench_name].append(result)
        logger.info(f"{self.recorder_key} from {result.begin_time} to {result.end_time}, result is {result.result}")

    def publish_results(self):
        publish_result = self.bus_client.get_publish_result()
        publish_result.put(self.results)

    def json_result_handler(self):
        pass