# encoding='utf-8'
import importlib
import sys
import time
from multiprocessing import Process
from haf.apihelper import Request, Response
from haf.apphelper import Stage, BasePage, save_screen_shot
from haf.asserthelper import AssertHelper
from haf.bench import HttpApiBench, BaseBench, AppBench, WebBench
from haf.busclient import BusClient
from haf.case import HttpApiCase, BaseCase, PyCase, AppCase, WebCase
from haf.common.database import SQLConfig
from haf.common.exception import FailRunnerException
from haf.common.log import Log
from haf.config import *
from haf.mark import locker, new_locker
from haf.result import HttpApiResult, AppResult, WebResult
from haf.suite import HttpApiSuite, AppSuite
from haf.utils import Utils
from haf.webhelper import *
import traceback
import asyncio

logger = Log.getLogger(__name__)


class Runner(Process):
    def __init__(self, log_dir: str, bus_client: BusClient, args):
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

    @locker
    def put_result(self,  key:str, result:HttpApiResult):
        logger.info(f"{self.key} : runner {self.pid} put result {result.case.ids.id}.{result.case.ids.subid}.{result.case.ids.name}", __name__)
        self.result_handler_queue.put(result)

    @locker
    def put_web_message(self, key:str):
        if self.args.web_server:
            if self.web_queue.full():
                self.web_queue.get()
            self.web_queue.put(self.runner)

    # TODO: try new_locker here, still need some tests
    # @locker 
    def put_case_back(self, key:str, case):
        logger.info(f"{self.runner_key} : runner put case {case.ids.id}.{case.ids.subid}-{case.ids.name}", __name__)
        with new_locker(self.bus_client, key):
            self.case_handler_queue.put(case)

    def result_handler(self, result):
        if isinstance(result, HttpApiResult) or isinstance(result, AppResult):
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
        elif isinstance(result, HttpApiCase) or isinstance(result, AppCase):
            self.runner["run"] = {
                f"{result.ids.id}.{result.ids.subid}-{result.ids.name}":
                {
                    "bench_name":result.bench_name
                }
            }
        # logger.info(f"{self.key} : runner {self.pid} -- put web message {self.runner}")
        self.put_web_message("web")

    def run(self):
        try:
            self.runner_key = f"{self.pid}$%runner$%"
            self.runner["key"] = f"{self.pid}"
            logger.bind_busclient(self.bus_client)
            logger.bind_process(self.pid)
            logger.info(f"{self.runner_key} start runner", __name__)
            self.web_queue = self.bus_client.get_publish_runner()
            self.case_handler_queue = self.bus_client.get_case()
            self.result_handler_queue = self.bus_client.get_result()
            loop = asyncio.get_event_loop()
            cases = []
            while True:
                flag = False
                if not self.case_handler_queue.empty() :
                    case = self.case_handler_queue.get()
                    if case == SIGNAL_CASE_END:
                        flag = True
                    if isinstance(case, HttpApiCase):
                        cases.append(case)
                        time.sleep(0.01)
                        if len(cases)>0 and (len(cases)>=3 or flag):
                            results = loop.run_until_complete(self.run_cases(cases))
                            for result in results:
                                if isinstance(result, (HttpApiResult, AppResult, WebResult)):
                                    self.put_result("result", result)
                            cases = []
                    elif isinstance(case, (AppCase, PyCase, WebCase)):
                        cases.append(case)
                        time.sleep(0.01)
                        if len(cases)>0 and (len(cases)>=1 or flag):
                            results = loop.run_until_complete(self.run_cases(cases))
                            for result in results:
                                if isinstance(result, (HttpApiResult, AppResult, WebResult)):
                                    self.put_result("result", result)
                            cases = []
                if flag:
                    break
            loop.close()
            self.end_handler()
        except Exception as e:
            logger.error(f"{self.key} : {e}", __name__)
            raise FailRunnerException

    async def run_cases(self, local_cases):
        done, pending = await asyncio.wait([self.run_case(local_case) for local_case in local_cases])
        results = []
        for r in done:
            results.append(r.result())
        return results

    async def run_case(self, local_case):
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
                logger.info(f"{self.key} : runner {self.pid} -- get {local_case.ids.id}.{local_case.ids.subid}-{local_case.ids.name}", __name__)
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
                
                result = await runner.run(local_case)

                if isinstance(result, list):
                    if result[0] == CASE_CAN_NOT_RUN_HERE:
                        self.put_case_back("case", local_case)
                        return
                    if result[0] == CASE_SKIP:
                        result = result[1]
                result.log_dir = f"{self.log_dir}/{local_case.bench_name}/{local_case.ids.id}.{local_case.ids.subid}.{local_case.ids.name}.log"
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

    def end_handler(self):
        logger.info(f"{self.runner_key} : end runner", __name__)
        self.result_handler_queue.put(SIGNAL_RESULT_END)
        self.case_handler_queue.put(SIGNAL_CASE_END)


class BaseRunner(object):
    def __init__(self, bench:BaseBench):
        self.bench = bench

    def check_case_run_here(self, case):
        if len(case.dependent) == 0:
            return True
        try:
            for dependence in case.dependent:
                if dependence not in self.bench.cases.keys():
                    return False

            return True
        except Exception:
            return False

    def check_case_run(self, case): # if skip, return False
        return case.run == CASE_RUN

    def check_case_error(self, case):
        return case.error == CASE_ERROR

    def get_dependence_case_from_bench(self, dependence):
        return None


class PyRunner(BaseRunner):
    def __init__(self, bench):
        super().__init__(bench)
        self.bench = bench
        self.key = ""

    async def run(self, case:PyCase):
        result = HttpApiResult()
        self.key = case.log_key
        result.on_case_begin()
        if not self.check_case_run(case): # not False is skip
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
                check_func(case.expect.sql_response_result, data, case.sqlinfo.check_list["sql_response"])
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
                png_before = save_screen_shot(driver, png_dir, f"{png_name}-before")
                self.run_stage(case, page, case.stages.get(key, Stage()), result)
                png_after = save_screen_shot(driver, png_dir, f"{png_name}-after")
                case.pngs[key] = {"before": f"./png/{png_name}-before.png", "after": f"./png/{png_name}-after.png"}
            result.case = case
            result.result = RESULT_PASS
            result.run_error = None
        except Exception as e:
            logger.error(f"{self.key} : {e}", __name__)
            result.run_error = e
            result.result = RESULT_ERROR
        result.on_case_end()
        return result

    def run_stage(self, case, page, stage: Stage=Stage(), result: AppResult=AppResult()):
        try:
            paths = stage.path
            operation = stage.operation
            logger.info(f"{self.key} -- {OPERATION_APP_ANTI_GROUP[operation]}", __name__)
            if  operation== OPERATION_APP_CLICK:
                page.click(paths)
            elif operation == OPERATION_APP_SENDKEYS:
                page.send_keys(paths, stage.info.get("keys"))
            elif operation == OPERATION_APP_SWIPE:
                page.swipe(stage.info.get("direction"))
            stage.result = "PASS"
            time.sleep(stage.time_sleep)
        except Exception as e:
            stage.result = str(e)
            if stage.show_try:
                stage.result = "PASS"
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
            driver = self.create_web_driver(case.desired_caps)
            logger.info(f"{self.key} : wait web {case.desired_caps.platformName} start ... [{case.time_sleep}s]", __name__)
            driver.get(case.desired_caps.start_url)
            driver.maximize_window()
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
                png_before = web_save_screen_shot(driver, png_dir, f"{png_name}-before")
                self.run_stage(case, page, case.stages.get(key, WebStage()), result)
                png_after = web_save_screen_shot(driver, png_dir, f"{png_name}-after")
                case.pngs[key] = {"before": f"./png/{png_name}-before.png", "after": f"./png/{png_name}-after.png"}
            result.case = case
            result.result = RESULT_PASS
            result.run_error = None
        except Exception as e:
            logger.error(f"{self.key} : {e}", __name__)
            result.run_error = e
            result.result = RESULT_ERROR
        result.on_case_end()
        return result

    def run_stage(self, case, page, stage: Stage=WebStage(), result: WebResult=WebResult()):
        try:
            paths = stage.path
            operation = stage.operation
            logger.info(f"{self.key} -- {OPERATION_WEB_ANTI_GROUP[operation]}", __name__)
            if  operation== OPERATION_WEB_CLICK:
                page.click(paths)
            elif operation == OPERATION_WEB_SENDKEYS:
                page.send_keys(paths, stage.info.get("keys"))
            elif operation == OPERATION_WEB_SWIPE:
                page.swipe(stage.info.get("direction"))
            stage.result = "PASS"
            time.sleep(stage.time_sleep)
        except Exception as e:
            stage.result = str(e)
            if stage.show_try:
                stage.result = "PASS"
                logger.warning(f"{self.key} : <<could failed stage>> : [{stage.id}] -- {e}", __name__)
            result.run_error = f"{stage.id} : {e}"
            if not stage.show_try:
                raise e
