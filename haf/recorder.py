# encoding='utf-8'
import time
from multiprocessing import Process

from haf.busclient import BusClient
from haf.case import HttpApiCase
from haf.common.exception import FailRecorderException
from haf.common.log import Log
from haf.result import HttpApiResult, EndResult, Detail
from haf.config import *
from haf.utils import Utils

logger = Log.getLogger(__name__)


class Recorder(Process):
    def __init__(self):
        super().__init__()
        self.bus_client = None
        self.daemon = True
        self.results = EndResult()
        self.recorder_key = ""

    def on_recorder_start(self):
        self.results.begin_time = Utils.get_datetime_now()

    def on_recorder_stop(self):
        self.results.end_time = Utils.get_datetime_now()

    def run(self):
        try:
            self.on_recorder_start()
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
        self.on_recorder_stop()
        self.publish_results()
        logger.info(f"{self.recorder_key} end recorder")
        self.json_result_handler()
        system_handler = self.bus_client.get_system()
        system_handler.put(SIGNAL_RECORD_END)

    def on_case_pass(self, suite_name):
        self.results.passed += 1
        if suite_name not in self.results.summary :
            self.results.summary[suite_name] = {"passed":1, "skip":0, "failed":0, "error":0}
        else:
            self.results.summary[suite_name]["passed"] += 1

    def on_case_skip(self, suite_name):
        self.results.skip += 1
        if suite_name not in self.results.summary :
            self.results.summary[suite_name] = {"passed":0, "skip":1, "failed":0, "error":0}
        else:
            self.results.summary[suite_name]["skip"] += 1

    def on_case_fail(self, suite_name):
        self.results.failed += 1
        if suite_name not in self.results.summary :
            self.results.summary[suite_name] = {"passed":0, "skip":0, "failed":1, "error":0}
        else:
            self.results.summary[suite_name]["failed"] += 1

    def on_case_error(self, suite_name):
        self.results.error += 1
        if suite_name not in self.results.summary :
            self.results.summary[suite_name] = {"passed":0, "skip":0, "failed":0, "error":1}
        else:
            self.results.summary[suite_name]["error"] += 1

    def check_case_result(self, result:HttpApiResult):
        suite_name = result.case.bench_name
        if result.result == RESULT_SKIP:
            self.on_case_skip(suite_name)
        elif result.result == RESULT_PASS:
            self.on_case_pass(suite_name)
        elif result.result == RESULT_FAIL:
            self.on_case_fail(suite_name)
        elif result.result == RESULT_ERROR:
            self.on_case_error(suite_name)

    def add_result_to_suite(self, result:HttpApiResult):
        if result.case.bench_name not in self.results.suite_name:
            self.results.suite_name.append(result.case.bench_name)
            case = result.case
            suite = Detail(case.bench_name)
            suite.begin_time = result.begin_time
            suite.end_time = result.end_time
            suite.cases.append(result)
        else:
            for suite in self.results.details.values():
                if suite.suite_name == result.case.bench_name:
                    suite = suite
                    break
            suite.end_time = result.end_time
            suite.cases.append(result)
        self.results.details[result.case.bench_name] = suite

    def result_handler(self, result:HttpApiResult):
        logger.info(f"{self.recorder_key} from {result.begin_time} to {result.end_time}, result is {result.result}")
        self.add_result_to_suite(result)
        self.check_case_result(result)
        self.publish_results()

    def publish_results(self):
        publish_result = self.bus_client.get_publish_result()
        publish_result.put(self.results.deserialize())

    def json_result_handler(self):
        pass