# encoding='utf-8'
import importlib
import json
import sys
import time
from multiprocessing import Process, Lock as m_lock
from threading import Thread, Lock as t_lock
from haf.apihelper import Request, Response
from haf.apphelper import Stage, BasePage, save_screen_shot
from haf.asserthelper import AssertHelper
from haf.bench import HttpApiBench, BaseBench, AppBench, WebBench, PyBench
from haf.busclient import BusClient
from haf.case import HttpApiCase, BaseCase, PyCase, AppCase, WebCase
from haf.common.database import SQLConfig
from haf.common.exception import FailRunnerException
from haf.common.log import Log
from haf.config import *
from haf.mark import locker, new_locker
from haf.result import HttpApiResult, AppResult, WebResult
from haf.suite import HttpApiSuite, AppSuite
from haf.utils import Utils, Signal, SignalThread
from haf.signal import Signal as SignalTemp
from haf.webhelper import *
import traceback
import asyncio

logger = Log.getLogger(__name__)


class Runner(Process):
    def __init__(self, log_dir: str, bus_client: BusClient, m_lock: list, args):
        super().__init__()
        self.daemon = True
        self.bus_client = bus_client
        self.benchs = {}
        self.bench = None
        self.key = ""
        self.runner_key = ""
        self.lock = False
        self.runner = {"get": 0, "skip": 0, "run": {}, "done":[], "key": 0}
        self.log_dir = log_dir
        self.args = args
        self.locks = m_lock
        '''
        locks [0] : get case lock
        locks [1] : put case back lock
        locks [2] : put result lock
        locks [3] : put web message lock
        '''

    def load(self):
        pass

    def init_runner(self, case: BaseCase):
        self.bench = self.get_bench(case)

    def get_bench(self, case: BaseCase):
        '''
        init bench, if exist, get bench
        :param case:
        :return:
        '''
        bench = self.benchs.get(case.bench_name, None)
        if bench is None :
            if isinstance(case, HttpApiCase):
                bench = HttpApiBench(self.args)
            elif isinstance(case, PyCase):
                bench = PyBench(self.args)
            elif isinstance(case, AppCase):
                bench = AppBench(self.args)
            elif isinstance(case, WebCase):
                bench = WebBench(self.args)
        
        bench.add_case(case)
        self.benchs[case.bench_name] = bench
        return bench

    @locker
    def put_result(self,  key: str, lock: m_lock=None, result: HttpApiResult=HttpApiResult()):
        '''
        put result to recorder, from runner to recorder, need lock
        :param key:
        :param lock:
        :param result:
        :return:
        '''
        logger.info(f"{self.key} : runner {self.pid} put result {result.case.ids.id}.{result.case.ids.subid}.{result.case.ids.name}", __name__)
        self.result_handler_queue.put(result)

    def put_web_message(self, key: str, lock: m_lock=None):
        '''
        put web message to web server
        :param key:
        :param lock:
        :return:
        '''

        with new_locker(self.bus_client, key, lock):
            if self.web_queue.full():
                self.web_queue.get()
            self.web_queue.put(self.runner)

    def put_case_back(self, key:str, case):
        '''
        put can not run case to loader to republish, from runner to loader, need lock
        :param key:
        :param case:
        :return:
        '''
        logger.info(f"{self.runner_key} : runner put case {case.ids.id}.{case.ids.subid}-{case.ids.name} for dependent : {case.dependent}", __name__)
        with new_locker(self.bus_client, key, self.locks[1]):
            self.case_back_queue.put(case)
        import random
        time.sleep(random.random())

    def result_handler(self, result):
        '''
        result handler
        :param result:
        :return:
        '''
        if isinstance(result, HttpApiResult) or isinstance(result, AppResult) or isinstance(result, WebResult):
            if result.case.run == CASE_SKIP:
                self.runner["skip"] += 1
            self.runner["run"] = {}
            self.runner["done"].append({
                f"{result.case.ids.id}.{result.case.ids.subid}-{result.case.ids.name}":
                {
                    "bench_name" : result.case.bench_name,
                    "begin" : result.begin_time,
                    "end" : result.end_time,
                    "result" : RESULT_GROUP.get(str(result.result))
                }
            })
        elif isinstance(result, HttpApiCase) or isinstance(result, AppCase) or isinstance(result, WebCase):
            self.runner["run"] = {
                f"{result.ids.id}.{result.ids.subid}-{result.ids.name}":
                {
                    "bench_name":result.bench_name
                }
            }
        logger.debug(f"{self.key} : runner {self.pid} -- put web message {self.runner}", __name__)
        self.put_web_message("web", self.locks[3])

    def signal_service(self):
        '''
        signal service to make runner run without enough cases
        :return:
        '''
        self.signal = Signal()
        self.st = SignalThread(self.signal, 0.2)
        self.st.start()
    
    def stop_signal(self):
        if self.st:
            self.st._stop()

    def run_loop(self, cases):
        '''
        TODO: need use aiohttp to make it work as async mode
        run loop, sync
        :param cases:
        :return:
        '''
        self.loop = asyncio.get_event_loop()
        results = self.loop.run_until_complete(self.run_cases(cases))
        for result in results:
            if isinstance(result, (HttpApiResult, AppResult, WebResult)):
                self.put_result("result", self.locks[2], result)

    def run(self):
        try:
            self.runner_key = f"{self.pid}$%runner$%"
            self.runner["key"] = f"{self.pid}"
            self.loop = None
            logger.bind_busclient(self.bus_client)
            logger.bind_process(self.pid)
            logger.set_output(self.args.local_logger, self.args.nout, self.args.debug)
            logger.info(f"{self.runner_key} start runner", __name__)

            self.web_queue = self.bus_client.get_publish_runner()
            self.case_handler_queue = self.bus_client.get_case()
            self.case_back_queue = self.bus_client.get_case_back()
            self.result_handler_queue = self.bus_client.get_result()

            self.signal_service()

            cases = []
            while True:
                case_end = False
                case = None
                if not self.case_handler_queue.empty() :
                    with new_locker(self.bus_client, "case_runner", self.locks[0]):
                        case = self.case_handler_queue.get()
                        logger.debug(f"get case from loader {case}", __name__)
                    if isinstance(case, SignalTemp) and case.signal == SIGNAL_CASE_END:
                        case_end = True
                    elif isinstance(case, (HttpApiCase, AppCase, PyCase, WebCase)):
                        cases.append(case)
                    logger.debug(f"cases' length is {len(cases)}, and end is {case}", __name__)

                if len(cases) > 0 and (len(cases) >= 1 or case_end or self.signal.signal):
                    logger.debug(f"cases' length is {len(cases)}, case_end is {case_end}, signal is {self.signal.signal}", __name__)
                    self.run_loop(cases)
                    cases = []
                if case_end:
                    break
                time.sleep(0.01)
            if self.loop: # here fix when cases is None, loop is None
                self.loop.close()
            self.end_handler()
        except Exception as e:
            logger.error(f"{self.key} : {e}", __name__)
            raise FailRunnerException

    async def run_cases(self, local_cases):
        '''
        run cases
        :param local_cases:
        :return:
        '''
        done, pending = await asyncio.wait([self.run_case(local_case) for local_case in local_cases])
        results = []
        for r in done:
            results.append(r.result())
        return results

    async def run_case(self, local_case):
        '''
        run case
        :param local_case:
        :return:
        '''
        if isinstance(local_case, HttpApiCase):
            result = HttpApiResult()
        elif isinstance(local_case, AppCase):
            result = AppResult()
        elif isinstance(local_case, PyCase):
            result = HttpApiResult()
        elif isinstance(local_case, WebCase):
            result = WebResult()
        try:
            try:
                self.key = local_case.log_key
                logger.info(f"{self.key} : runner {self.pid} -- get case {type(local_case)} <{local_case.ids.id}.{local_case.ids.subid}-{local_case.ids.name}>", __name__)
                self.result_handler(local_case)
                self.init_runner(local_case)
                if local_case.type == CASE_TYPE_HTTPAPI:
                    runner = ApiRunner(self.bench)
                elif local_case.type == CASE_TYPE_PY:
                    runner = PyRunner(self.bench)
                elif local_case.type == CASE_TYPE_APP:
                    runner = AppRunner(self.bench, self.log_dir)
                elif local_case.type == CASE_TYPE_WEBUI:
                    runner = WebRunner(self.bench, self.log_dir)
                logger.debug(f"{self.key} : running now")
                result = await runner.run(local_case)

                if isinstance(result, list):
                    if result[0] == CASE_CAN_NOT_RUN_HERE:
                        self.put_case_back("case_back", local_case)
                        return
                    if result[0] == CASE_SKIP:
                        result = result[1]

                result.log_dir = f"{self.get_log_path(self.log_dir)}/{local_case.bench_name}/{local_case.ids.id}.{local_case.ids.subid}.{local_case.ids.name}.log"
                result.bind_runner(self.pid)
                self.result_handler(result)
                return result
            except Exception as runerror:
                logger.error(f"{self.key} : {runerror}", __name__)
                result.run_error = traceback.format_exc()
                result.result = RESULT_ERROR
                return result
        except Exception as e:
            logger.error(f"{self.key} : {e}", __name__)
            result.run_error = traceback.format_exc()
            result.result = RESULT_ERROR
            return result

    def get_log_path(self, log_path):
        if isinstance(log_path, str):
            if log_path.startswith("."):
                return f"{os.path.abspath(log_path)}"
            else:
                return log_path

    def end_handler(self):
        '''
        send result end and case end signal to main/loader, from runner to main
        :return:
        '''
        logger.info(f"{self.runner_key} : end runner", __name__)
        self.result_handler_queue.put(SignalTemp(self.pid, SIGNAL_RESULT_END))
        self.case_handler_queue.put(SignalTemp(self.pid, SIGNAL_CASE_END))


class BaseRunner(object):
    def __init__(self, bench:BaseBench):
        self.bench = bench

    def check_case_run_here(self, case):
        '''
        check case can run here or not
        :param case:
        :return:
        '''
        logger.debug(f"check_case_run_here Base Runner check case run here {case.dependent}", __name__)
        check_case_run_here_result = False
        if not case.dependent or len(case.dependent) == 0:
            check_case_run_here_result = True
            return check_case_run_here_result
        elif isinstance(case.dependent, list) and case.dependent==['None']:
            check_case_run_here_result = True
            return check_case_run_here_result
        try:
            for dependence in case.dependent:
                if dependence not in self.bench.cases.keys():
                    check_case_run_here_result = False
                    return check_case_run_here_result
            if isinstance(case, HttpApiCase):
                self.get_dependent_var(case)
            check_case_run_here_result = True
            return check_case_run_here_result
        except Exception:
            check_case_run_here_result = False
        return check_case_run_here_result

    def check_case_filter(self, case):
        '''
        check case is in the filter
        :param case:
        :return:
        '''
        filter_cases = self.bench.args.filter_case
        check_case_filter_result = False
        if filter_cases is None or filter_cases=='None':
            check_case_filter_result = True
        elif isinstance(filter_cases, list):
            check_case_filter_result = case.ids.name in filter_cases
        else:
            check_case_filter_result = True
        logger.debug(f"check_case_filter case <{case.ids.name}> check in [{self.bench.args.filter_case}], result is {check_case_filter_result}", __name__)
        return check_case_filter_result

    def check_case_run(self, case): # if skip, return False
        if self.check_case_filter(case):
            return case.run == CASE_RUN
        else:
            return False

    def check_case_error(self, case):
        return case.error == CASE_ERROR

    def get_dependence_case_from_bench(self, dependent):
        '''
        get dependency
        :param dependent:
        :return:
        '''
        logger.debug(f"get_dependence_case_from_bench : {dependent}", __name__)
        return self.bench.cases.get(dependent)

    def reuse_with_dependent(self, new_attr):
        '''
        TODO: not complete
        :param new_attr:
        :return:
        '''
        logger.debug(f"reuse_with_dependent type is {type(new_attr)}", __name__)
        if isinstance(new_attr, dict):
            return self.replace_dict(new_attr)
        elif isinstance(new_attr, list):
            return self.replace_list(new_attr)

    def replace_str(self, data):
        logger.debug(f"replace str here {type(data)} : {data}", __name__)
        begin = "<@begin@>"
        end = "<@end@>"
        if isinstance(data, str):
            f, temp = data.split("<@begin@>")
            temp, l = temp.split("<@end@>")
            temp = json.loads(temp.replace("'", '"'))
            logger.debug(f"replace_str {temp}", __name__)
            dependent_case = self.get_dependence_case_from_bench(f"{temp.get('case')}")
            replace_target = ""
            if isinstance(dependent_case, (HttpApiCase, PyCase, AppCase, WebCase)):
                if temp.get("type") in ["int", "str", "list", "dict"]:
                    logger.debug(f"case is {dependent_case}", __name__)
                    temp_property = temp.get("property")
                    for i in range(1, len(temp_property)+1):
                        if i==1:
                            current_pp = temp_property.get(str(i))
                            if current_pp == "api_response":
                                replace_target = dependent_case.response
                        else:
                            current_pp = temp_property.get(str(i))
                            if isinstance(replace_target, Response):
                                replace_target = getattr(replace_target, current_pp)
                            elif isinstance(replace_target, dict):
                                replace_target = replace_target.get(current_pp)
                        logger.debug(f"replace_str {i} : {replace_target}")
                    logger.debug(f"replace_str target found is {replace_target}", __name__)

            elif temp.get("type") in ["find_table_index"]:
                logger.debug(f"case is {dependent_case}", __name__)
                replace_target = Utils.find_table_index(temp.get("table_name"),
                                                        (int(temp.get("range").get("start")), int(temp.get("range").get("end"))),
                                                        temp.get("data"))
                logger.debug(f"replace_str target found is {replace_target}", __name__)


            return f"{f}{replace_target}{l}"

    def replace_dict(self, data):
        for key in data.keys():
            logger.debug(f"replace_dict check key {key} here: {data.get(key)}", __name__)
            current_data = data.get(key)
            if current_data is None:
                return data
            if "<@begin@>" in str(current_data):
                if isinstance(current_data, str):
                    data[key] = self.replace_str(current_data)
                elif isinstance(current_data, list):
                    data[key] = self.replace_list(current_data)
        return data

    def replace_list(self, data):
        for i, data_i in enumerate(data):
            logger.debug(f"replace_list check data {i} here: {data_i}", __name__)
            current_data = data_i
            if current_data is None:
                return data
            if "<@begin@>" in str(current_data):
                if isinstance(current_data, str):
                    data[i] = self.replace_str(current_data)
                elif isinstance(current_data, list):
                    data[i] = self.replace_list(current_data)
        logger.debug(f"replace_list : {data}", __name__)
        return data

    def get_dependent_var(self, case):
        try:
            logger.debug(f"dependent var is {case.dependent_var}", __name__)
            if isinstance(case, (HttpApiCase)):
                if case.dependent_var is None:
                    return
                else:
                    for dv in case.dependent_var:
                        if dv in ["request_data", "request_header"]:
                            logger.debug(f"start get dependent {dv}", __name__)
                            request = case.request
                            if dv == "request_header":
                                header = request.header
                                request.header = self.reuse_with_dependent(header)
                            elif dv == "request_data":
                                data = request.data
                                request.data = self.reuse_with_dependent(data)

                        if dv in ["sql_response"]:
                            logger.debug(f"start get dependent {dv}", __name__)
                            sql_info = case.sqlinfo
                            if dv == "sql_response":
                                sql_response = sql_info.scripts.get("sql_response")
                                sql_info.scripts["sql_response"] = self.reuse_with_dependent(sql_response)
        except Exception as e:
            logger.error(e, __name__)
            traceback.print_exc()
            raise e


class PyRunner(BaseRunner):
    def __init__(self, bench):
        super().__init__(bench)
        self.bench = bench
        self.key = ""

    async def run(self, case:PyCase):
        result = HttpApiResult()
        self.key = case.log_key
        result.on_case_begin()

        if not self.check_case_run_here(case) :
            logger.debug(f"PyRunner check_case_run_here : Dependent not found ! get False", __name__)
            result.on_case_end()
            return [CASE_CAN_NOT_RUN_HERE, result]
        if not self.check_case_run(case): # not False is skip
            logger.debug(f"PyRunner check_case_run False", __name__)
            result.case = case
            result.on_case_end()
            result.result = RESULT_SKIP
            return [CASE_SKIP, result]

        result.case = case
        logger.info(f"{self.key} : PyRunner run - {case.bench_name} {case.ids.id}.{case.ids.subid}-{case.ids.name}", __name__)
        suite = HttpApiSuite()
        try:
            module_name = case.module_name
            module_path = case.module_path
            sys.path.append(module_path)
            module = importlib.import_module(module_name)
            suite = getattr(module, case.suite)()
            func = getattr(suite, case.func)
            case.request = getattr(suite, "request", Request())
            if case.param is not None:
                func(case.param)
            else:
                func()
            case.response = getattr(suite, "response", Response())
            result.result = RESULT_PASS
        except AssertionError as ae:
            case.response = getattr(suite, "response", Response())
            traceback.print_exc()
            logger.error(f"{self.key} : {traceback.format_exc()}", __name__)
            result.result = RESULT_FAIL
            result.run_error = traceback.format_exc()
            result.on_case_end()
            return result
        except Exception as e:
            traceback.print_exc()
            logger.error(f"{self.key} : {traceback.format_exc()}", __name__)
            result.result = RESULT_ERROR
            result.run_error = traceback.format_exc()
            result.on_case_end()
            return result

        result.on_case_end()
        return result


class ApiRunner(BaseRunner):
    '''
    ApiRunner
    '''
    def __init__(self, bench:HttpApiBench):
        super().__init__(bench)
        self.bench = bench
        self.key = ""

    async def run(self, case:HttpApiCase):
        '''
        run the HttpApiCase
        :param case: HttpApiCase
        :return: result: HttpApiResult
        '''
        self.key = case.log_key
        result = HttpApiResult()
        result.on_case_begin()
        if not self.check_case_run_here(case) :
            result.on_case_end()
            return [CASE_CAN_NOT_RUN_HERE, result]
        if not self.check_case_run(case): # not False is skip
            result.case = case
            result.on_case_end()
            result.result = RESULT_SKIP
            return [CASE_SKIP, result]
        logger.info(f"{self.key} : ApiRunner run - {case.ids.id}.{case.ids.subid}-{case.ids.name}", __name__)
        try:
            result.case = case
            case.response = self.request(case.request)
            result.result_check_response = self.check_response(case.response, case.expect.response)
            case.expect.sql_response_result = self.sql_response(case.sqlinfo.scripts["sql_response"], case.sqlinfo.config, case.sqlinfo.check_list["sql_response"])
            temp_r = self.check_sql_response(case)
            result.result_check_sql_response = temp_r[0]
            if not temp_r[0]:
                result.run_error = temp_r[1]
            result.case = case
            result.result = RESULT_PASS if False not in result.result_check_response and result.result_check_sql_response is True else RESULT_FAIL
        except Exception as e:
            logger.error(f"{self.key} : {e}", __name__)
            result.run_error = e
            result.result = RESULT_ERROR
        result.on_case_end()
        return result

    def request(self, request:Request):
        return Utils.http_request(request, key=self.key)

    def sql_response(self, sql_script:str, sql_config:SQLConfig, check_list:list):
        if sql_config is None or sql_script is None:
            return None

        if check_list is None:
            sql_result = Utils.sql_execute(sql_config, sql_script, dictcursor=True, key=self.key)
        else:
            sql_result = Utils.sql_execute(sql_config, sql_script, key=self.key)
        return sql_result

    def check_response(self, response:Response, response_expect:Response):
        result = True
        result_check_code = result and AssertHelper.assert_that(response.code, 200, key=self.key)
        if response_expect.body == {}:
            result_check_body = True
        else:
            result_check_body = AssertHelper.assert_that(response.body, response_expect.body, key=self.key)
        return [result_check_code, result_check_body]

    def check_sql_response(self, case:HttpApiCase):
        '''
        check sql == response, use case's third function
        :param case:
        :return:
        '''
        try:
            result = [True, "ok"]
            if case.expect.sql_check_func is None or case.expect.sql_response_result is None:
                return [True, "ok"]
            data = case.response.body
            logger.info(f"{self.key} : check sql response : {case.expect.sql_check_func}", __name__)
            class_content = importlib.import_module(case.expect.sql_check_func[0])
            check_func = getattr(getattr(class_content, case.expect.sql_check_func[1]), case.expect.sql_check_func[2])
            logger.info(f"{self.key} : check func : {check_func}", __name__)
            logger.info(f"{self.key} : check list is {case.sqlinfo.check_list}", __name__)
            if case.sqlinfo.check_list is not None:
                check_func(case.expect.sql_response_result, data, case.sqlinfo.check_list["sql_response"], testcase=case)
            else:
                check_func(case.expect.sql_response_result, data)
        except Exception as e:
            logger.error(f"{self.key} : {e}", __name__)
            traceback.print_exc()
            return [False, traceback.format_exc()]
        return result


class AppRunner(BaseRunner):
    '''
    AppRunner
    '''
    def __init__(self, bench:AppBench, log_dir):
        super().__init__(bench)
        self.bench = bench
        self.key = ""
        self.log_dir = log_dir

    def wait_activity(self, activity, timeout, driver):
        """Wait for an activity: block until target activity presents
        or time out.
        This is an Android-only method.
        :Agrs:
        - activity - target activity
        - timeout - max wait time, in seconds
        - interval - sleep interval between retries, in seconds
        """
        try:
            i = 0
            while i<timeout:
                logger.info(f"{self.key}: current activity is {driver.current_activity}", __name__)
                if driver.current_activity == activity:
                    return
                time.sleep(1)
                i += 1
        except Exception as e:
            logger.error(f"{self.key}: {e}", __name__)
            return 

    async def run(self, case: AppCase):
        '''
        run the AppCase
        :param case: AppCase
        :return: result: AppResult
        '''
        self.key = case.log_key
        result = AppResult()
        result.on_case_begin()
        if not self.check_case_run_here(case) :
            result.on_case_end()
            return [CASE_CAN_NOT_RUN_HERE, result]
        if not self.check_case_run(case): # not False is skip
            result.case = case
            result.on_case_end()
            result.result = RESULT_SKIP
            return [CASE_SKIP, result]

        logger.info(f"{self.key} : AppRunner run - {case.ids.id}.{case.ids.subid}-{case.ids.name}", __name__)
        try:
            result.case = case
            from appium import webdriver
            driver = webdriver.Remote(APP_DRIVER_PATH, case.desired_caps.deserialize())
            logger.info(f"{self.key} : wait app start ... [{case.time_sleep}s]", __name__)
            if case.wait_activity:
                time.sleep(5)
                self.wait_activity(case.wait_activity, case.time_sleep, driver)
            else:
                time.sleep(case.time_sleep)
            logger.info(f"{self.key} : driver is {driver}", __name__)
            page = BasePage(driver)
            for key in range(1, len(case.stages.keys())+1):
                logger.info(f"{self.key} : {key} == {case.stages.get(key).deserialize()}", __name__)
                png_dir = f"{self.log_dir}"
                png_name = f"{case.bench_name}.{case.ids.id}.{case.ids.subid}.{case.ids.name}.{key}"
                case.pngs[key] = {"before": f"./png/{png_name}-before.png", "after": f"./png/{png_name}-after.png"}
                png_before = save_screen_shot(driver, png_dir, f"{png_name}-before")
                self.run_stage(case, page, case.stages.get(key, Stage()), result)
                png_after = save_screen_shot(driver, png_dir, f"{png_name}-after")
            result.case = case
            result.result = RESULT_PASS
            result.run_error = None
        except Exception as e:
            logger.error(f"{self.key} : {e}", __name__)
            result.run_error = e
            # TODO : make the result to error and fail
            result.result = RESULT_FAIL # RESULT_ERROR, fix #134
        result.on_case_end()
        return result

    def run_operation(self, page, operation, paths, info):
        '''
        run the appium stages
        :param page:
        :param operation:
        :param paths:
        :param info:
        :return:
        '''
        if  operation== OPERATION_APP_CLICK:
            page.click(paths)
        elif operation == OPERATION_APP_SENDKEYS:
            page.send_keys(paths, info.get("keys"))
        elif operation == OPERATION_APP_SWIPE:
            page.swipe(info.get("direction"))

    def run_stage(self, case, page, stage: Stage=Stage(), result: AppResult=AppResult()):
        count_now = 0
        try:
            paths = stage.path
            operation = stage.operation
            logger.info(f"{self.key} -- {OPERATION_APP_ANTI_GROUP[operation]}", __name__)
            info = stage.info
            run_count = stage.run_count
            stage.result = []
            if isinstance(run_count, int):
                for x in range(1, run_count+1):
                    logger.info(f"{self.key} -- {stage.id} - {OPERATION_APP_ANTI_GROUP[operation]} - {x}", __name__)
                    count_now = x
                    self.run_operation(page, operation, paths, info)
                    stage.result.append(f"{x}-PASS")
            else:
                self.run_operation(page, operation, paths, info)
            if run_count == 1 or run_count is None:
                stage.result = "PASS"
            elif run_count == 0:
                stage.result = "SKIP"
            time.sleep(stage.time_sleep)
        except Exception as e:
            stage.result = str(e)
            if stage.show_try:
                stage.result = "PASS [can fail]"
                logger.warning(f"{self.key} : <<could failed stage>> : [{stage.id}] -- {e}", __name__)
            result.run_error = f"{stage.id} : {e}"
            if not stage.show_try:
                raise e


class WebRunner(BaseRunner):
    '''
    WebRunner
    '''
    def __init__(self, bench: WebBench, log_dir):
        super().__init__(bench)
        self.bench = bench
        self.key = ""
        self.log_dir = log_dir

    def wait_activity(self, activity, timeout, driver):
        """Wait for an activity: block until target activity presents
        or time out.
        This is an Android-only method.
        :Agrs:
        - activity - target activity
        - timeout - max wait time, in seconds
        - interval - sleep interval between retries, in seconds
        """
        try:
            i = 0
            while i<timeout:
                logger.info(f"{self.key}: current activity is {driver.current_activity}", __name__)
                if driver.current_activity == activity:
                    return
                time.sleep(1)
                i += 1
        except Exception as e:
            logger.error(f"{self.key}: {e}", __name__)
            return 
    
    def create_web_driver(self, desired_caps: WebDesiredCaps):
        from selenium import webdriver
        if desired_caps.platformName == "chrome":
            return webdriver.Chrome()
        elif desired_caps.platformName == "firefox":
            return webdriver.Firefox()
        elif desired_caps.platformName == "ie":
            return webdriver.Ie()
        elif desired_caps.platformName == "safari":
            return webdriver.Safari()
        elif desired_caps.platformName == "opera":
            return webdriver.Opera()

    async def run(self, case: WebCase):
        '''
        run the AppCase
        :param case: AppCase
        :return: result: AppResult
        '''
        self.key = case.log_key
        result = WebResult()
        result.on_case_begin()

        if not self.check_case_run_here(case) :
            result.on_case_end()
            return [CASE_CAN_NOT_RUN_HERE, result]

        if not self.check_case_run(case): # not False is skip
            result.case = case
            result.on_case_end()
            result.result = RESULT_SKIP
            return [CASE_SKIP, result]

        logger.info(f"{self.key} : WebRunner run - {case.ids.id}.{case.ids.subid}-{case.ids.name}", __name__)
        try:
            result.case = case
            self.driver = self.create_web_driver(case.desired_caps)
            logger.info(f"{self.key} : wait web {case.desired_caps.platformName} start ... [{case.time_sleep}s]", __name__)
            self.driver.get(case.desired_caps.start_url)
            self.driver.maximize_window()
            if case.wait_activity:
                time.sleep(5)
                self.wait_activity(case.wait_activity, case.time_sleep, self.driver)
            else:
                time.sleep(case.time_sleep)
            logger.info(f"{self.key} : driver is {self.driver}", __name__)
            page = BasePage(self.driver)
            for key in range(1, len(case.stages.keys())+1):
                logger.info(f"{self.key} : {key} == {case.stages.get(key).deserialize()}", __name__)
                png_dir = f"{self.log_dir}"
                png_name = f"{case.bench_name}.{case.ids.id}.{case.ids.subid}.{case.ids.name}.{key}"
                case.pngs[key] = {"before": f"./png/{png_name}-before.png", "after": f"./png/{png_name}-after.png"}
                png_before = web_save_screen_shot(self.driver, png_dir, f"{png_name}-before")
                self.run_stage(case, page, case.stages.get(key, WebStage()), result)
                png_after = web_save_screen_shot(self.driver, png_dir, f"{png_name}-after")
            result.case = case
            result.result = RESULT_PASS
            result.run_error = None
        except Exception as e:
            logger.error(f"{self.key} : {e}", __name__)
            result.run_error = e
            # TODO : make the result to error and fail
            result.result = RESULT_FAIL # RESULT_ERROR, fix #134
        finally:
            result.on_case_end()
            if self.driver:
                try:
                    self.driver.close()
                except Exception as e:
                    pass
            return result

    def run_operation(self, page, operation, paths, info):
        '''
        run the appium stages
        :param page:
        :param operation:
        :param paths:
        :param info:
        :return:
        '''
        if  operation== OPERATION_WEB_CLICK:
            page.click(paths)
        elif operation == OPERATION_WEB_SENDKEYS:
            page.send_keys(paths, info.get("keys"))
        elif operation == OPERATION_WEB_SWIPE:
            page.swipe(info.get("direction"))

    def run_stage(self, case, page, stage: WebStage=WebStage(), result: WebResult=WebResult()):
        count_now = 0
        try:
            paths = stage.path
            operation = stage.operation
            logger.info(f"{self.key} -- {OPERATION_WEB_ANTI_GROUP[operation]}", __name__)
            info = stage.info
            run_count = stage.run_count
            stage.result = []
            if isinstance(run_count, int):
                for x in range(1, run_count+1):
                    logger.info(f"{self.key} -- {stage.id} - {OPERATION_WEB_ANTI_GROUP[operation]} - {x}", __name__)
                    count_now = x
                    self.run_operation(page, operation, paths, info)
                    stage.result.append(f"{x}-PASS")
            else:
                self.run_operation(page, operation, paths, info)
            if run_count == 1 or run_count is None:
                stage.result = "PASS"
            elif run_count == 0:
                stage.result = "SKIP"
            time.sleep(stage.time_sleep)
        except Exception as e:
            stage.result = str(e)
            if stage.show_try:
                stage.result = "PASS [can fail]"
                logger.warning(f"{self.key} : <<could failed stage>> : [{stage.id}] -- {e}", __name__)
            result.run_error = f"{stage.id} : {e}"
            if not stage.show_try:
                raise e
