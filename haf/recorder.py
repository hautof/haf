# encoding='utf-8'

import time
from multiprocessing import Process, Lock as m_lock
from haf.busclient import BusClient
from haf.case import HttpApiCase, BaseCase, PyCase, WebCase, AppCase
from haf.common.database import SQLConfig
from haf.common.exception import FailRecorderException
from haf.common.log import Log
from haf.result import HttpApiResult, EndResult, Detail, Summary, AppResult, WebResult
from haf.config import *
from haf.mark import locker, new_locker
from haf.pluginmanager import plugin_manager
from haf.utils import Utils
from haf.signal import Signal
from haf.ext.jinjia2report.report import Jinja2Report

logger = Log.getLogger(__name__)


class Recorder(Process):
    '''
    recorder process
    '''
    def __init__(self, bus_client: BusClient, runner_count: int=1, case_name:str="", time_str: str="", log_dir="", report_template_path="base", lock: m_lock=None, args=None):
        super().__init__()
        self.bus_client = bus_client
        self.args = args
        self.daemon = True
        self.results = EndResult(f"{case_name}-{time_str}")
        self.runner_count = runner_count
        self.signal_end_count = 0
        self.report_path = self.args.report_output_dir if self.args.report_output_dir else "./data/report.html"
        self.case_name = case_name
        self.recorder_key = ""
        self.log_dir = log_dir
        self.report_template_path = report_template_path
        self.complete_case_count = 0
        self.lock = lock

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
            logger.bind_process(self.pid)
            logger.set_output(self.args.local_logger, self.args.nout, self.args.debug)
            logger.info(f"{self.recorder_key} start recorder ", __name__)
            #self.bus_client = BusClient()
            self.results_handler = self.bus_client.get_result()
            self.publish_result = self.bus_client.get_publish_result()
            self.publish_result_main = self.bus_client.get_case_result_main()
            self.case_count = self.bus_client.get_case_count()
            while True:
                if not self.results_handler.empty() :
                    result = self.results_handler.get()
                    logger.debug(f"receive message -- {result}", __name__)
                    # get result from runner to recorder
                    if isinstance(result, (HttpApiResult, AppResult, WebResult)):
                        if isinstance(result.case, (HttpApiCase, BaseCase, PyCase, WebCase, AppCase)):
                            logger.info(f"{self.recorder_key} {result.case.bench_name}.{result.case.ids.id}.{result.case.ids.subid}.{result.case.ids.name} is {RESULT_GROUP.get(str(result.result), None)}", __name__)
                        else:
                            logger.info(f"{self.recorder_key} recorder ! wrong result!", __name__)
                            logger.info(f"{self.recorder_key} recorder {result.run_error}", __name__)
                        self.complete_case_count += 1
                        self.result_handler(result)
                    # check the runner end or not, from runner to recorder, need check signal count
                    elif isinstance(result, Signal) and result.signal == SIGNAL_RESULT_END:
                        self.signal_end_count += 1
                        logger.debug(f"receive message -- {self.signal_end_count}", __name__)
                        if self.runner_count == self.signal_end_count:
                            self.end_handler()
                            break
                time.sleep(0.001)
        except Exception:
            raise FailRecorderException

    def generate_report(self):
        '''
        generate report
        :return:
        '''
        report = Jinja2Report.report(self.results, name=self.report_template_path)
        Jinja2Report.write_report_to_file(report, self.report_path)
        report = Jinja2Report.report(self.results, name=self.report_template_path)
        Jinja2Report.write_report_to_file(report, f"{self.log_dir}/report.html")
        self.generate_export_report()

    def generate_export_report(self):
        '''
        generate email export report
        :return:
        '''
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
        '''
        when recorder end, publish results
        :return:
        '''
        logger.debug("on record handle end", __name__)
        self.on_recorder_stop()
        self.publish_results()
        self.generate_report()
        self.show_in_cs()
        self.publish_to_mysql()
        logger.info(f"{self.recorder_key} end recorder", __name__)
        self.send_record_end_signal()

    def send_record_end_signal(self):
        '''
        send end signal, from recorder to logger/main
        :return:
        '''
        logger.info(f"{self.recorder_key} send record end signal to main", __name__)
        system_handler = self.bus_client.get_system()
        system_handler.put(Signal(self.pid, SIGNAL_RECORD_END))
        logger_end = self.bus_client.get_logger_end()
        logger_end.put(Signal(self.pid, SIGNAL_LOGGER_END))

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
        '''
        check case's result is ok or not
        :param result:
        :return:
        '''
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

    @locker
    def count_case(self, key: str, lock: m_lock=None):
        '''
        put case's commplete count to loader, from recorder to loader
        :param key:
        :param lock:
        :return:
        '''
        logger.debug(f"put case count {self.complete_case_count}", __name__)
        self.case_count.put(self.complete_case_count)

    def result_handler(self, result):
        '''
        result handler, include add to suite,check case result, publish result
        :param result:
        :return:
        '''
        self.count_case(self.recorder_key, self.lock)
        self.add_result_to_suite(result)
        self.check_case_result(result)
        self.publish_results()

    def publish_results(self):
        '''
        publish results to web server
        :return:
        '''
        logger.debug(f"publish results now...", __name__)
        if hasattr(self.args, "web_server") and self.args.web_server:
            if self.publish_result.full():
                self.publish_result.get()
            self.publish_result.put(self.results)
        if self.publish_result_main.full():
            self.publish_result_main.get()
        self.publish_result_main.put(self.results)

    # show end results here before publish to mysql
    def show_in_cs(self):
        '''
        show case in command
        :return:
        '''
        result_summary = "|{:^8}|{:^8}|{:^8}|{:^8}|{:^8}|".format(self.results.passed, self.results.failed, self.results.skip, self.results.error, \
            self.results.all)
        if not self.args.nout:
            logger.info("----------------------------------------------", __name__)
            logger.info("|--\33[32mPASS\33[0m--|--\33[31mFAIL\33[0m--|--\33[37mSKIP\33[0m--|--\33[35mERROR\33[0m-|---\33[36mALL\33[0m--|", __name__)
            logger.info(result_summary, __name__)
            logger.info("----------------------------------------------", __name__)
        else:
            print("----------------------------------------------")
            print("|--\33[32mPASS\33[0m--|--\33[31mFAIL\33[0m--|--\33[37mSKIP\33[0m--|--\33[35mERROR\33[0m-|---\33[36mALL\33[0m--|")
            print(result_summary)
            print("----------------------------------------------")

    def publish_to_mysql(self):
        '''
        publish results to mysql database
        '''
        logger.info("publish result to sql", __name__)
        plugin_manager.publish_to_sql(self.args, self.results)

