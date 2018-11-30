# encoding='utf-8'
import json
import time
from multiprocessing import Process

from haf.busclient import BusClient
from haf.case import HttpApiCase
from haf.common.exception import FailRecorderException
from haf.common.log import Log
from haf.result import HttpApiResult, EndResult, Detail
from haf.config import *
from haf.utils import Utils
from haf.ext.jinjia2report.report import Jinja2Report

logger = Log.getLogger(__name__)


class Recorder(Process):
    def __init__(self, runner_count:int=1, report_path:str="", case_name:str=""):
        super().__init__()
        self.bus_client = None
        self.daemon = True
        self.results = EndResult(f"AutoTest-{case_name}")
        self.runner_count = runner_count
        self.signal_end_count = 0
        self.report_path = report_path
        self.case_name = case_name
        self.recorder_key = ""

    def on_recorder_start(self):
        self.results.begin_time = Utils.get_datetime_now()

    def on_recorder_stop(self):
        self.results.end_time = Utils.get_datetime_now()
        self.results.duration = Utils.get_date_result(self.results.begin_time, self.results.end_time)
        for suite_name in self.results.summary.keys():
            for key in ("begin_time", "end_time", "duration"):
                self.results.summary[suite_name][key] = getattr(self.results.details.get(suite_name), key)

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
                            logger.info(f"{self.recorder_key} recorder--{result.case.bench_name}.{result.case.ids.id}.{result.case.ids.subid}.{result.case.ids.name} is {result.result}")
                        else:
                            logger.info(f"{self.recorder_key} recorder ! wrong result!")
                            logger.info(f"{self.recorder_key} recorder {result.run_error}")
                        self.result_handler(result)
                    elif result == SIGNAL_RESULT_END:
                        self.signal_end_count += 1
                        if self.runner_count == self.signal_end_count:
                            self.end_handler()
                            break
                time.sleep(0.1)
        except Exception:
            raise FailRecorderException

    def generate_report(self):
        Jinja2Report.write_report_to_file(Jinja2Report.report(self.results), self.report_path)

    def end_handler(self):
        self.on_recorder_stop()
        self.publish_results()
        self.generate_report()
        logger.info(f"{self.recorder_key} end recorder")
        self.json_result_handler()
        system_handler = self.bus_client.get_system()
        system_handler.put(SIGNAL_RECORD_END)

    def on_case_pass(self, suite_name):
        self.results.passed += 1
        self.results.all += 1
        self.results.summary[suite_name]["passed"] += 1
        self.results.summary[suite_name]["all"] += 1

    def on_case_skip(self, suite_name):
        self.results.skip += 1
        self.results.all += 1
        self.results.summary[suite_name]["skip"] += 1
        self.results.summary[suite_name]["all"] += 1

    def on_case_fail(self, suite_name):
        self.results.failed += 1
        self.results.all += 1
        self.results.summary[suite_name]["failed"] += 1
        self.results.summary[suite_name]["all"] += 1

    def on_case_error(self, suite_name):
        self.results.error += 1
        self.results.all += 1
        self.results.summary[suite_name]["error"] += 1
        self.results.summary[suite_name]["all"] += 1

    def check_case_result(self, result:HttpApiResult):
        suite_name = result.case.bench_name
        if suite_name not in self.results.summary.keys():
            self.results.summary[suite_name] = {"passed": 0, "skip": 0, "failed": 0, "error": 0, "all": 0, "base_url":result.case.request.host_port}
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
            suite.duration = Utils.get_date_result(suite.begin_time, suite.end_time)
            suite.cases.append(result)
        self.results.details[result.case.bench_name] = suite

    def result_handler(self, result:HttpApiResult):
        logger.info(f"{self.recorder_key} from {result.begin_time} to {result.end_time}, result is {result.result}")
        self.add_result_to_suite(result)
        self.check_case_result(result)
        self.publish_results()

    def publish_results(self):
        publish_result = self.bus_client.get_publish_result()
        if publish_result.full():
            publish_result.get()
        publish_result.put(self.results)

    def json_result_handler(self):
        return json.dumps(self.results.deserialize())