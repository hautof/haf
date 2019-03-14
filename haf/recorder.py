# encoding='utf-8'

import time
from multiprocessing import Process

from haf.busclient import BusClient
from haf.case import HttpApiCase, BaseCase, PyCase, WebCase, AppCase
from haf.common.database import SQLConfig
from haf.common.exception import FailRecorderException
from haf.common.log import Log
from haf.result import HttpApiResult, EndResult, Detail, Summary, AppResult, WebResult
from haf.config import *
from haf.utils import Utils
from haf.ext.jinjia2report.report import Jinja2Report

logger = Log.getLogger(__name__)


class Recorder(Process):
    def __init__(self, bus_client: BusClient, sql_config: SQLConfig, sql_publish: bool=False, runner_count: int=1, report_path:str="", case_name:str="", log_dir="", report_template_path="base", args=None):
        super().__init__()
        self.bus_client = bus_client
        self.args = args
        self.daemon = True
        self.results = EndResult(f"haf-{case_name}")
        self.runner_count = runner_count
        self.signal_end_count = 0
        self.report_path = report_path
        self.case_name = case_name
        self.recorder_key = ""
        self.log_dir = log_dir
        self.report_template_path = report_template_path
        self.sql_config = sql_config
        self.sql_publish =  sql_publish

    def on_recorder_start(self):
        '''
        recorder start time
        '''
        self.results.begin_time = Utils.get_datetime_now()

    def on_recorder_stop(self):
        '''
        recorder stop time
        '''
        self.results.end_time = Utils.get_datetime_now()
        self.results.duration = Utils.get_date_result(self.results.begin_time, self.results.end_time)
        for suite_name in self.results.summary.keys():
            self.results.summary[suite_name].begin_time = getattr(self.results.details.get(suite_name), "begin_time")
            self.results.summary[suite_name].end_time = getattr(self.results.details.get(suite_name), "end_time")
            self.results.summary[suite_name].duration = getattr(self.results.details.get(suite_name), "duration")

    def run(self):
        try:
            self.on_recorder_start()
            self.recorder_key = f"{self.pid}$%recorder$%"
            logger.bind_busclient(self.bus_client)
            logger.info(f"{self.recorder_key} start recorder ")
            #self.bus_client = BusClient()
            self.results_handler = self.bus_client.get_result()
            self.publish_result = self.bus_client.get_publish_result()
            while True:
                if not self.results_handler.empty() :
                    result = self.results_handler.get()
                    if isinstance(result, (HttpApiResult, AppResult, WebResult)):
                        if isinstance(result.case, (HttpApiCase, BaseCase, PyCase, WebCase, AppCase)):
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
        report = Jinja2Report.report(self.results, name=self.report_template_path)
        Jinja2Report.write_report_to_file(report, self.report_path)
        report = Jinja2Report.report(self.results, name=self.report_template_path)
        Jinja2Report.write_report_to_file(report, f"{self.log_dir}/report.html")
        self.generate_export_report()

    def generate_export_report(self):
        if self.args:
            if hasattr(self.args, "report_export_template") and self.args.report_export_template:
                report = Jinja2Report.report(self.results, name=self.args.report_export_template)
            else:
                report = Jinja2Report.report(self.results, name="base_email")
            if hasattr(self.args, "report_export_dir") and self.args.report_export_dir:
                Jinja2Report.write_report_to_file(report, f"{self.args.report_export_dir}")
            else:
                Jinja2Report.write_report_to_file(report, f"{self.log_dir}/report-export.html")

    def end_handler(self):
        self.on_recorder_stop()
        self.publish_results()
        self.generate_report()
        self.publish_to_mysql()
        logger.info(f"{self.recorder_key} end recorder")
        self.send_record_end_signal()

    def send_record_end_signal(self):
        system_handler = self.bus_client.get_system()
        system_handler.put(SIGNAL_RECORD_END)

    def on_case_pass(self, suite_name):
        self.results.passed += 1
        self.results.all += 1
        self.results.summary[suite_name].passed += 1
        self.results.summary[suite_name].all += 1

    def on_case_skip(self, suite_name):
        self.results.skip += 1
        self.results.all += 1
        self.results.summary[suite_name].skip += 1
        self.results.summary[suite_name].all += 1

    def on_case_fail(self, suite_name):
        self.results.failed += 1
        self.results.all += 1
        self.results.summary[suite_name].failed += 1
        self.results.summary[suite_name].all += 1

    def on_case_error(self, suite_name):
        self.results.error += 1
        self.results.all += 1
        self.results.summary[suite_name].error += 1
        self.results.summary[suite_name].all += 1

    def check_case_result(self, result):
        suite_name = result.case.bench_name
        if suite_name not in self.results.summary.keys():
            self.results.summary[suite_name] = Summary(suite_name, result.case.request.host_port if isinstance(result, HttpApiResult) else None)
        if result.result == RESULT_SKIP:
            self.on_case_skip(suite_name)
        elif result.result == RESULT_PASS:
            self.on_case_pass(suite_name)
        elif result.result == RESULT_FAIL:
            self.on_case_fail(suite_name)
        elif result.result == RESULT_ERROR:
            self.on_case_error(suite_name)

    def add_result_to_suite(self, result):
        '''
        add result to suite which case belong to.
        '''
        if result.case.bench_name not in self.results.suite_name:
            self.results.suite_name.append(result.case.bench_name)
            case = result.case
            suite = Detail(case.bench_name)
            suite.begin_time = result.begin_time
        else:
            # find suite here
            for suite in self.results.details.values():
                if suite.suite_name == result.case.bench_name:
                    suite = suite
                    break
        suite.end_time = result.end_time
        suite.duration = Utils.get_date_result(suite.begin_time, suite.end_time)
        suite.cases.append(result)
        self.results.details[result.case.bench_name] = suite

    def result_handler(self, result):
        logger.info(f"{self.recorder_key} from {result.begin_time} to {result.end_time}, result is {RESULT_GROUP.get(str(result.result), None)}")
        self.add_result_to_suite(result)
        self.check_case_result(result)
        self.publish_results()

    def publish_results(self):
        # logger.info(f"publish results now...")
        if self.publish_result.full():
            self.publish_result.get()
        self.publish_result.put(self.results)

    def publish_to_mysql(self):
        '''
        publish results to mysql database
        '''
        if self.sql_publish:
            logger.info(f"publish results {self.results} to mysql!")
            import_ok = False
            try:
                from hafsqlpublish.publish import Publish
                import_ok = True
            except Exception as e:
                logger.error("Plugin hafsqlpublish is not installed, using 'pip install hafsqlpublish -U' to install")
            if import_ok:
                publish = Publish(self.sql_config)
                publish.publish_result(self.results)

