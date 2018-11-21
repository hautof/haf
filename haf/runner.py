# encoding='utf-8'
import time
from multiprocessing import Process

from haf.common.database import SQLConfig

from haf.bench import HttpApiBench

import haf

from haf.apihelper import Request, Response
from haf.busclient import BusClient
from haf.result import HttpApiResult
from haf.common.log import Log
from haf.config import *
from haf.utils import Utils
from haf.asserthelper import AssertHelper
from haf.case import HttpApiCase

logger = Log.getLogger(__name__)


class Runner(Process):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.bus_client = None

    def load(self):
        pass

    def run(self):
        logger.debug("start runner {} ".format(self.pid))
        self.bus_client = BusClient()
        while True:
            case_handler = self.bus_client.get_case()
            if not case_handler.empty() :
                case = case_handler.get()
                if case == SIGNAL_CASE_END:
                    self.end_handler()
                    break
                result = self.run_case(case)
                result_handler = self.bus_client.get_result()
                result_handler.put(result)
            time.sleep(0.1)

    def run_case(self, local_case:HttpApiCase):
        result = HttpApiResult()
        try:
            try:
                if local_case.type == CASE_TYPE_HTTPAPI:
                    logger.debug("runner {} -- get {}.{}-{}".format(self.pid, local_case.ids.id, local_case.ids.subid, local_case.ids.name))
                    logger.debug(self.bus_client.get_bench().get(local_case.bench_name))
                    logger.debug(local_case.bench_name)
                    bench = self.bus_client.get_bench().get(local_case.bench_name)
                    api_runner = ApiRunner(bench)
                    result = api_runner.run(local_case)
            except Exception as runerror:
                logger.error(runerror)
            return result
        except Exception as e:
            logger.error(e)
            result.result = e
            return result

    def end_handler(self):
        logger.debug("end runner {} ".format(self.pid))
        result_handler = self.bus_client.get_result()
        result_handler.put(SIGNAL_RESULT_END)
        case_handler = self.bus_client.get_case()
        case_handler.put(SIGNAL_CASE_END)


class ApiRunner(object):
    '''
    ApiRunner
    '''
    def __init__(self, bench:HttpApiBench):
        self.bench = bench

    def run(self, case:HttpApiCase):
        '''
        run the HttpApiCase
        :param case: HttpApiCase
        :return: result: HttpApiResult
        '''
        logger.debug("ApiRunner run - {}.{}-{}".format(case.ids.id, case.ids.subid, case.ids.name))
        result = HttpApiResult()
        result.on_case_begin()
        case.response = self.request(case.request)
        case.expect.sql_response_result = self.sql_response(case.sqlinfo.scripts, self.bench.get_db(case.sqlinfo.config))
        result.case = case
        result.result_check_response = self.check_response(case.response, case.expect.response)
        result.result = result.result_check_response and result.result_check_sql_response
        result.on_case_end()
        return result

    def request(self, request:Request):
        return Utils.http_request(request)

    def sql_response(self, sql_script:str, sql_config:SQLConfig):
        sql_result = Utils.sql_execute(sql_config, sql_script)
        print(sql_result)
        return sql_result

    def check_response(self, response:Response, response_expect:Response):
        result = True
        result = result and AssertHelper.assert_that(response.code, 200) and AssertHelper.assert_that(response.body, response_expect.body)
        return result

    def check_sql_response(self, response:Response, sql_result):
        return True

