# encoding='utf-8'
import time
from multiprocessing import Process
from haf.bench import HttpApiBench
from haf.busclient import BusClient
from haf.common.database import SQLConfig
from haf.case import HttpApiCase, PyCase, AppCase, WebCase
from haf.common.exception import FailLoaderException
from haf.common.log import Log
from haf.config import *
from haf.utils import Utils
from haf.mark import locker

logger = Log.getLogger(__name__)


class Loader(Process):
    def __init__(self, bus_client:BusClient=None, args:list=None):
        super().__init__()
        self.bus_client = bus_client
        self.daemon = True
        self.key = ""
        self.loader = {"all":0, "error":0, "error_info":{}}

    def run(self):
        try:
            logger.bind_process(self.pid)
            self.key = f"{self.pid}$%loader$%"
            logger.bind_busclient(self.bus_client)
            logger.info(f"{self.key} start loader", __name__)
            self.case_queue = self.bus_client.get_case()
            while True:
                if self.get_parameter() == SIGNAL_START:
                    logger.info(f"{self.key} -- get start signal from main", __name__)
                    break
                time.sleep(0.01)

            while True:
                temp = self.get_parameter()
                if temp == SIGNAL_STOP :
                    while True:
                        if self.case_queue.empty():
                            self.end_handler()
                            return

                if temp is None:
                    time.sleep(0.01)
                    continue

                file_name = temp.get("file_name")
                inputs = LoadFromConfig.load_from_file(file_name)

                logger.debug(f"{self.key} -- {inputs}", __name__)
                input = inputs.get("config")[0]
                bench_name = input.get("name")
                module_name = input.get("module_name")
                module_path = input.get("module_path")

                bench = HttpApiBench()
                if "dbconfig" in inputs.keys():
                    for input in inputs.get("dbconfig"):
                        db = SQLConfig()
                        db.constructor(input)
                        bench.add_db(db)

                for input in inputs.get("testcases"):

                    if input.get("id") is None or input.get("subid") is None:
                        continue
                    if input.get("host_port") is None:
                        input["host_port"] = inputs.get("config")[0].get("host_port")
                    if "api_name" in input.keys():
                        case = HttpApiCase()
                    elif input.get("type") == "app":
                        case = AppCase()
                    elif input.get("type") == "web":
                        case = WebCase()
                    else:
                        case = PyCase(module_name, module_path)
                    try:
                        case.constructor(input)
                        case.bind_bench(bench_name)
                        case.sqlinfo.bind_config(bench.get_db(case.sqlinfo.config_id))
                    except Exception as e:
                        case.bind_bench(bench_name)
                        case.sqlinfo.bind_config(bench.get_db(case.sqlinfo.config_id))
                        case.run = CASE_SKIP
                        case.error = CASE_ERROR
                        case.error_msg = str(e)
                    self.add_case(case)
                    self.put_case("case", case)
                    self.put_web_message("web")

                self.put_web_message("web")
                time.sleep(0.01)
        except Exception as e:
            logger.error(f"{self.key} {e}", __name__)
            logger.error(f"{self.key} {FailLoaderException}", __name__)
            self.end_handler(e)

    def get_parameter(self, param_key=None):
        params_queue = self.bus_client.get_param()
        if not params_queue.empty():
            params = params_queue.get()
            if param_key is not None:
                return params.get(param_key)
            return params
        return None

    def add_case(self, case):
        self.loader["all"] += 1
        if case.error_msg != "":
            self.loader["error"] += 1
            self.loader["error_info"][f"{case.ids.id}.{case.ids.subid}.{case.ids.name}"] = case.error_msg

    @locker
    def put_web_message(self, key:str):
        web_queue = self.bus_client.get_publish_loader()
        if web_queue.full():
            web_queue.get()
        web_queue.put(self.loader)

    @locker
    def put_case(self, key:str, case):
        logger.info(f"{self.key} -- put case {case.bench_name} - {case.ids.id}.{case.ids.subid}.{case.ids.name}", __name__)
        self.case_queue.put(case)

    def end_handler(self, error=None):
        try:
            if error:
                logger.error(f"{self.key} end loader with Error - {error}", __name__)
            else:
                logger.info(f"{self.key} end loader", __name__)
            self.case_queue.put(SIGNAL_CASE_END)
        except Exception as e:
            logger.error(f"{self.key} {e}", __name__)


class LoadFromConfig(object):

    @staticmethod
    def load_from_file(file_name):
        if file_name.endswith(".xlsx"):
            output = LoadFromConfig.load_from_xlsx(file_name)
        elif file_name.endswith(".json"):
            output = LoadFromConfig.load_from_json(file_name)
        elif file_name.endswith(".yml"):
            output = LoadFromConfig.load_from_yml(file_name)
        elif file_name.endswith(".py"):
            output = LoadFromConfig.load_from_py(file_name)
        return output

    @staticmethod
    def load_from_xlsx(file_name):
        if isinstance(file_name, str):
            inputs = Utils.get_rows_from_xlsx(file_name)
            return inputs

    @staticmethod
    def load_from_json(file_name):
        if isinstance(file_name, str):
            inputs = Utils.load_from_json(file_name)
            return inputs

    @staticmethod
    def load_from_yml(file_name):
        if isinstance(file_name, str):
            inputs = Utils.load_from_yml(file_name)
            return inputs

    @staticmethod
    def load_from_py(file_name):
        if isinstance(file_name, str):
            inputs = Utils.load_from_py(file_name)
            return inputs