# encoding='utf-8'
import time
import haf
from multiprocessing import Process, Lock as m_lock
from haf.bench import HttpApiBench
from haf.busclient import BusClient
from haf.common.database import SQLConfig
from haf.case import HttpApiCase, PyCase, AppCase, WebCase
from haf.common.exception import FailLoaderException
from haf.common.log import Log
from haf.config import *
from haf.utils import Utils
from haf.mark import locker, new_locker
from haf.pluginmanager import plugin_manager
from haf.signal import Signal
from progress.bar import ChargingBar

logger = Log.getLogger(__name__)


class Loader(Process):
    '''
    loader
    '''
    def __init__(self, bus_client: BusClient=None, lock: m_lock=None, args: list=None):
        super().__init__()
        self.bus_client = bus_client
        self.daemon = True
        self.key = ""
        self.true_case_count = 0
        self.loader = {"all":0, "error":0, "error_info":{}}
        self.lock = lock
        self.args = args

    def run(self):
        '''
        loader run
        :return:
        '''
        try:
            logger.bind_process(self.pid)
            self.key = f"{self.pid}$%loader$%"
            logger.bind_busclient(self.bus_client)
            logger.set_output(self.args.local_logger, self.args.nout, self.args.debug)
            logger.info(f"{self.key} start loader", __name__)
            self.case_queue = self.bus_client.get_case()
            self.case_back_queue = self.bus_client.get_case_back()
            self.case_count = self.bus_client.get_case_count()
            self.web_queue = self.bus_client.get_publish_loader()
            self.params_queue = self.bus_client.get_param()

            # check the signal of start
            while True:
                signal_params_ = self.get_parameter()
                if isinstance(signal_params_, Signal) and signal_params_.signal == SIGNAL_START:
                    logger.info(f"{self.key} -- get start signal from main", __name__)
                    break

            if self.args.nout:
                cb = ChargingBar(max=100)
            complete_case_count = 0
            show_count = []
            all_count = []
            # check the params
            while True:
                temp = self.get_parameter()
                # check the signal of stop, after stop nothing!
                if isinstance(temp, Signal) and temp.signal == SIGNAL_STOP :
                    while True:
                        if not self.case_count.empty():
                            complete_case_count = self.case_count.get()
                            if complete_case_count not in all_count:
                                all_count.append(complete_case_count)
                        else:
                            pass
                        if self.args.nout:
                            cb.goto(complete_case_count*100/self.true_case_count)
                        if self.case_back_queue.empty():
                            pass
                        else:
                            logger.debug("put case here from back queue", __name__)
                            self.put_case("case", None, self.case_back_queue.get())

                        if self.case_queue.empty() and self.case_back_queue.empty():
                            with new_locker(self.bus_client, self.key, self.lock):
                                if complete_case_count not in show_count:
                                    logger.debug(f"complete case count check here {complete_case_count} == {self.true_case_count}", __name__)
                                    show_count.append(complete_case_count)
                                if complete_case_count==self.true_case_count:
                                    if self.args.nout:
                                        cb.finish()
                                    self.end_handler()
                                    return
                    time.sleep(0.01)
                elif temp is None:
                    time.sleep(0.01)
                    continue
                else:
                    file_name = temp.get("file_name")
                    logger.debug(f"file_name = {file_name}", __name__)
                    inputs = plugin_manager.load_from_file(file_name)

                    logger.debug("inputs", __name__)
                    logger.debug(f"{self.key} -- {inputs}", __name__)
                    input = inputs.get("config")[0]
                    bench_name = input.get("name")
                    module_name = input.get("module_name")
                    module_path = input.get("module_path")

                    logger.debug("bench", __name__)
                    bench = HttpApiBench(self.args)
                    if "dbconfig" in inputs.keys():
                        for input in inputs.get("dbconfig"):
                            db = SQLConfig()
                            db.constructor(input)
                            bench.add_db(db)

                    for input in inputs.get("testcases"):
                        logger.debug(input, __name__)
                        if input.get("id") is None or input.get("subid") is None:
                            continue
                        if input.get("host_port") is None:
                            input["host_port"] = inputs.get("config")[0].get("host_port")
                        if "api_name" in input.keys() or input.get("type")=="api":
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

                        self.true_case_count += 1
                        self.add_case(case)
                        self.put_case("case", None, case)
                        self.put_web_message("web")

                self.put_web_message("web")
        except Exception as e:
            logger.error(f"{self.key} {e}", __name__)
            logger.error(f"{self.key} {FailLoaderException}", __name__)
            import traceback
            traceback.print_exc()
            logger.error(f"{self.key} {traceback.format_exc()}",__name__)
            self.end_handler(e)

    def check_case_complete(self, key: str, lock=None):
        '''
        check case  complete count and the all case count
        :param key:
        :param lock:
        :return:
        '''
        if not self.case_count.empty():
            complete_case_count = self.case_count.get()
            if complete_case_count==self.true_case_count:
                return True
        return False

    def get_parameter(self, param_key=None):
        '''
        get the param from queue, which send by main program in program
        :param param_key:
        :return:
        '''
        if not self.params_queue.empty():
            params = self.params_queue.get()
            if param_key is not None:
                return params.get(param_key)
            return params
        return None

    def add_case(self, case):
        '''
        add case to message of publish web server
        :param case:
        :return:
        '''
        self.loader["all"] += 1
        if case.error_msg != "":
            self.loader["error"] += 1
            self.loader["error_info"][f"{case.ids.id}.{case.ids.subid}.{case.ids.name}"] = case.error_msg

    def put_web_message(self, key: str, lock=None):
        '''
        put message to web server queue when web enable
        :param key:
        :param lock:
        :return:
        '''
        if hasattr(self.args, "web_server") and self.args.web_server:
            if self.web_queue.full():
                self.web_queue.get()
            self.web_queue.put(self.loader)

    def put_case(self, key: str, lock, case):
        '''
        put case to case queue, from loader to runners
        :param key:
        :param lock:
        :param case:
        :return:
        '''
        logger.info(f"{self.key} -- put case {case.bench_name} - {case.ids.id}.{case.ids.subid}.{case.ids.name}", __name__)
        self.case_queue.put(case)

    def end_handler(self, error=None):
        '''
        when catch the stop signal, end loader, and send the case_end signal
        :param error:
        :return:
        '''
        try:
            if error:
                logger.error(f"{self.key} end loader with Error - {error}", __name__)
            else:
                logger.info(f"{self.key} end loader", __name__)
            self.case_queue.put(Signal(self.pid, SIGNAL_CASE_END))
        except Exception as e:
            logger.error(f"{self.key} {e}", __name__)
