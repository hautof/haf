# encoding='utf-8'
import time
from multiprocessing import Process, Manager

from haf.common.database import SQLConfig

from haf.bench import HttpApiBench
from haf.busclient import BusClient
from haf.case import HttpApiCase
from haf.common.exception import FailLoaderException
from haf.common.log import Log
from haf.config import *
from haf.suite import HttpApiSuite
from haf.utils import Utils

logger = Log.getLogger(__name__)


class Loader(Process):
    def __init__(self):
        super().__init__()
        self.bus_client = None
        self.daemon = True

    def run(self):
        try:
            self.bus_client = BusClient()
            logger.info("start loader {} ".format(self.pid))

            while True:
                if self.get_parameter() == SIGNAL_START:
                    logger.info("loader {} -- get {}".format(self.pid, "start from main"))
                    break
                time.sleep(0.1)

            while True:
                temp = self.get_parameter()
                if temp == SIGNAL_STOP :
                    while True:
                        case_queue = self.bus_client.get_case()
                        if case_queue.empty():
                            self.end_handler()
                            return

                if temp is None:
                    time.sleep(0.1)
                    continue

                file_name = temp.get("file_name")
                inputs = LoadFromConfig.load_from_file(file_name)

                suite = HttpApiSuite()

                bench_name = ""

                input = inputs.get("config")[0]
                bench_name = input.get("name")

                bench = HttpApiBench()

                for input in inputs.get("dbconfig"):
                    db = SQLConfig()
                    db.constructor(input)
                    bench.add_db(db)

                for input in inputs.get("testcases"):
                    case = HttpApiCase()
                    case.constructor(input)
                    case.bind_bench(bench_name)
                    case.sqlinfo.bind_config(bench.get_db(case.sqlinfo.config_id))
                    self.put_case(case)

                time.sleep(0.1)
        except Exception:
            raise FailLoaderException

    def get_parameter(self, param_key=None):
        params_queue = self.bus_client.get_param()
        if not params_queue.empty():
            params = params_queue.get()
            if param_key is not None:
                return params.get(param_key)
            return params
        return None

    def put_case(self, case):
        logger.info("loader {} -- put case {}.{}.{}".format(self.pid, case.ids.id, case.ids.subid, case.ids.name))
        case_queue = self.bus_client.get_case()
        case_queue.put(case)

    def end_handler(self):
        try:
            logger.info("end loader {} ".format(self.pid))
            case_queue = self.bus_client.get_case()
            case_queue.put(SIGNAL_CASE_END)
        except Exception as e:
            logger.error(e)
        pass



class LoadFromConfig(object):

    @staticmethod
    def load_from_file(file_name):
        if file_name.endswith(".xlsx"):
            return LoadFromConfig.load_from_xlsx(file_name)
        elif file_name.endswith(".json"):
            return LoadFromConfig.load_from_json(file_name)

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