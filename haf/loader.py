# encoding='utf-8'
import time
from multiprocessing import Process

from haf.bench import HttpApiBench
from haf.busclient import BusClient
from haf.case import HttpApiCase
from haf.common.log import Log
from haf.config import *
from haf.utils import Utils

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
            params_queue = self.bus_client.get_param()
            if not params_queue.empty():
                param = params_queue.get()
                if param == SIGNAL_START:
                    logger.debug("loader {} -- get {}".format(self.pid, "start from main"))
                    break
            time.sleep(0.1)

        while True:
            params_queue = self.bus_client.get_param()
            if not params_queue.empty():
                param = params_queue.get()
                file_name = param.get("file_name")
                if file_name is None:
                    continue
                inputs = LoadFromConfig.load_from_xlsx(file_name)

                benchs = self.bus_client.get_bench()
                print(benchs)
                benchs.set("test", HttpApiBench())
                for input in inputs.get("testcases"):
                    case_queue = self.bus_client.get_case()
                    case = HttpApiCase()
                    case.constructor(input)
                    logger.debug("loader {} -- put {}".format(self.pid, case))
                    case_queue.put(case)
                break
            time.sleep(0.1)

        self.end_handler()

    def end_handler(self):
        try:
            logger.debug("end loader {} ".format(self.pid))
            case_queue = self.bus_client.get_case()
            case_queue.put(SIGNAL_CASE_END)
        except Exception as e:
            logger.error(e)
        pass

class LoadFromConfig(object):

    @staticmethod
    def load_from_xlsx(file_name):
        if isinstance(file_name, str):
            inputs = Utils.get_rows_from_xlsx(file_name)
            return inputs
        if isinstance(file_name, list):
            pass

    @staticmethod
    def load_from_json(file_name):
        if isinstance(file_name, str):
            pass

        if isinstance(file_name, list):
            pass