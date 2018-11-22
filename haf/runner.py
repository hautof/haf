# encoding='utf-8'
import importlib
import sys
import time
from multiprocessing import Process

from haf.common.database import SQLConfig

from haf.bench import HttpApiBench, BaseBench

from haf.apihelper import Request, Response
from haf.busclient import BusClient
from haf.common.exception import FailRunnerException
from haf.result import HttpApiResult
from haf.common.log import Log
from haf.config import *
from haf.utils import Utils
from haf.asserthelper import AssertHelper
from haf.case import HttpApiCase, BaseCase
import traceback

logger = Log.getLogger(__name__)


class Runner(Process):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.bus_client = None
        self.benchs = {}
        self.bench = None

    def load(self):
        pass

    def init_runner(self, case:BaseCase):
        self.bench = self.get_bench(case)

    def get_bench(self, case:BaseCase):
        bench = self.benchs.get(case.bench_name, None)
        if bench is None :
            bench = HttpApiBench()
        bench.add_case(case)
        self.benchs[case.bench_name] = bench
        return bench

    def put_result(self, result:HttpApiResult):
        logger.info("runner {} put result {} ".format(self.pid, result))
        result_handler = self.bus_client.get_result()
        result_handler.put(result)

    def run(self):
        try:
            logger.info("start runner {} ".format(self.pid))
            self.bus_client = BusClient()
            while True:
                case_handler = self.bus_client.get_case()
                if not case_handler.empty() :
                    case = case_handler.get()
                    if case == SIGNAL_CASE_END:
                        self.end_handler()
                        break
                    self.run_case(case)
                time.sleep(0.1)
        except Exception as e:
            logger.error(e)
            raise FailRunnerException

    def run_case(self, local_case:HttpApiCase):
        result = HttpApiResult()
        try:
            try:
                if local_case.type == CASE_TYPE_HTTPAPI:
                    logger.info("runner {} -- get {}.{}-{}".format(self.pid, local_case.ids.id, local_case.ids.subid, local_case.ids.name))
                    self.init_runner(local_case)
                    api_runner = ApiRunner(self.bench)
                    result = api_runner.run(local_case)
                    if isinstance(result, list):
                        if result[0] == CASE_CAN_NOT_RUN_HERE:
                            self.put_case_back(local_case)
                            return
                        if result[0] == CASE_SKIP:
                            result = result[1]
            except Exception as runerror:
                traceback.print_exc()
                result.run_error = runerror
            self.put_result(result)
        except Exception as e:
            logger.error(e)
            result.result = e
            return result

    def end_handler(self):
        logger.info("end runner {} ".format(self.pid))
        result_handler = self.bus_client.get_result()
        result_handler.put(SIGNAL_RESULT_END)
        case_handler = self.bus_client.get_case()
        case_handler.put(SIGNAL_CASE_END)

    def put_case_back(self, case):
        logger.info("runner {} put case {}.{}-{}".format(self.pid, case.ids.id, case.ids.subid, case.ids.name))
        case_handler = self.bus_client.get_case()
        case_handler.put(case)
        time.sleep(1)


class BaseRunner(object):
    def __init__(self, bench:BaseBench):
        self.bench = bench

    def check_case_run_here(self, case):
        if len(case.dependent) == 0:
            return True
        try:
            print(self.bench.cases.keys())
            for dependence in case.dependent:
                print(dependence)
                if dependence not in self.bench.cases.keys():
                    return False

            return True
        except Exception:
            return False

    def check_case_skip(self, case):
        return case.run


class ApiRunner(BaseRunner):
    '''
    ApiRunner
    '''
    def __init__(self, bench:HttpApiBench):
        super().__init__(bench)
        self.bench = bench

    def run(self, case:HttpApiCase):
        '''
        run the HttpApiCase
        :param case: HttpApiCase
        :return: result: HttpApiResult
        '''
        result = HttpApiResult()
        result.on_case_begin()
        if not self.check_case_run_here(case) :
            result.on_case_end()
            return [CASE_CAN_NOT_RUN_HERE, result]
        if not self.check_case_skip(case):
            result.case = case
            result.on_case_end()
            result.result = CASE_SKIP
            return [CASE_SKIP, result]

        logger.info("ApiRunner run - {}.{}-{}".format(case.ids.id, case.ids.subid, case.ids.name))
        case.response = self.request(case.request)
        case.expect.sql_response_result = self.sql_response(case.sqlinfo.scripts["sql_response"], case.sqlinfo.config, case.sqlinfo.check_list["sql_response"])
        result.result_check_sql_response = self.check_sql_response(case)
        result.case = case
        result.result_check_response = self.check_response(case.response, case.expect.response)
        result.result = result.result_check_response and result.result_check_sql_response
        result.on_case_end()
        return result

    def request(self, request:Request):
        return Utils.http_request(request)

    def sql_response(self, sql_script:str, sql_config:SQLConfig, check_list:list):
        if sql_config is None or sql_script is None:
            return None

        if check_list is None:
            sql_result = Utils.sql_execute(sql_config, sql_script, dictcursor=True)
        else:
            sql_result = Utils.sql_execute(sql_config, sql_script)
        return sql_result

    def check_response(self, response:Response, response_expect:Response):
        result = True
        result = result and AssertHelper.assert_that(response.code, 200) and AssertHelper.assert_that(response.body, response_expect.body)
        return result

    def check_sql_response(self, case:HttpApiCase):
        '''
        check sql == response, use case's third function
        :param case:
        :return:
        '''
        if case.expect.sql_check_func is None or case.expect.sql_response_result is None:
            return False
        result = True
        data = case.response.body
        logger.info("check sql response : {}".format(case.expect.sql_check_func))
        class_content = importlib.import_module(case.expect.sql_check_func[0])
        check_func = getattr(getattr(class_content, case.expect.sql_check_func[1]), case.expect.sql_check_func[2])
        logger.info("check func : {}".format(check_func))

        if case.sqlinfo.check_list is not None:
            result = check_func(case.expect.sql_response_result, data, case.sqlinfo.check_list["sql_response"])
        else:
            result = check_func(case.expect.sql_response_result, data)

        return result

