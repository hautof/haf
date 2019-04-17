# encoding='utf-8'
'''
file name : case.py
desc : the cases
others :
    usage :
        py case must implement BaseCase
        class TestApi(BaseCase):

'''
import json

from haf.apihelper import Request, Response, Ids, Expect, SqlInfo
from haf.apphelper import Stage, AppIds, DesiredCaps
from haf.config import *
from haf.common.log import Log
from haf.webhelper import *

logger = Log.getLogger(__name__)


class BaseCase(object):
    '''
    BaseCase the base of cases
    '''
    def __init__(self):
        self.mark = CASE_MARK_BASE
        self.name = None
        self.id = None
        self.subid = None
        self.type = None
        self.expect = None
        self.run = True
        self.bench_name = ""
        self.error_msg = ""
        self.AttrNoneList = ["result", "error", "AttrNoneList", ]
        self.func = None


class PyCase(BaseCase):
    '''
    py cases
    '''
    def __init__(self, module_name, module_path):
        super().__init__()
        self.mark = CASE_MARK_API
        self.type = CASE_TYPE_PY
        self.message_type = MESSAGE_TYPE_CASE
        self.log_key = ""
        self.module_name = module_name
        self.module_path = module_path
        self.suite = ""
        self.func = ""
        self._init_all()
        self.run = self.func
        self.param = None

    def _init_all(self):
        '''
        init all py case's needed
        :return:
        '''
        self.ids = Ids()
        self.run = CASE_RUN
        self.dependent = []
        self.bench_name = ""
        self.request = Request()
        self.expect = Expect()
        self.response = Response()
        self.sqlinfo = SqlInfo()
        self.log_key = ""
        self.error = None

    def constructor(self, *args, **kwargs):
        '''
        :param args:
        :param kwargs:
        :return:
        '''
        args_init = {}
        if len(args) > 0 and isinstance(args[0], dict):
            args_init = args[0]
        else:
            args_init = kwargs
        #logger.info(args_init)
        self.ids.constructor(args_init)
        self.run = CASE_RUN if args_init.get("run") is True else CASE_SKIP
        self.func = args_init.get("func")
        self.suite = args_init.get("suite")
        self.param = args_init.get("param")
        temp = args_init.get("request")
        self.request = temp if temp else Request()

    def bind_bench(self, bench_name):
        '''
        bind bench with bench name
        :param bench_name:
        :return:
        '''
        self.bench_name = bench_name
        self.generate_log_key()

    def generate_log_key(self):
        '''
        generate log key to self
        :return:
        '''
        self.log_key = self.key = f"{self.bench_name}$%{self.ids.id}.{self.ids.subid}.{self.ids.name}$%"

    def deserialize(self):
        '''
        return the dict type of pycase
        :return:
        '''
        return {
            "ids": self.ids.deserialize(),
            "run": self.run,
            "bench_name": self.bench_name,
            "func": str(self.func),
            "type": self.type,
            "suite": self.suite,
            "param": str(self.param),
            "module_name": self.module_name,
            "module_path": self.module_path,
            "sqlinfo": self.sqlinfo.deserialize()
        }


class HttpApiCase(BaseCase):
    '''
    http api case
    '''
    def __init__(self):
        super().__init__()
        self.mark = CASE_MARK_API
        self.type = CASE_TYPE_HTTPAPI
        self.message_type = MESSAGE_TYPE_CASE
        self.log_key = ""
        self._init_all()

    def _init_all(self):
        '''
        init all api case needed
        :return:
        '''
        self.ids = Ids()
        self.run = CASE_RUN
        self.dependent = []
        self.dependent_var = []
        self.bench_name = ""
        self.request = Request()
        self.expect = Expect()
        self.response = Response()
        self.sqlinfo = SqlInfo()
        self.log_key = ""
        self.error = None

    def constructor(self, *args, **kwargs):
        '''
        :param args:
        :param kwargs:
        :return:
        '''
        args_init = {}
        if len(args) > 0 and isinstance(args[0], dict):
            args_init = args[0]
        else:
            args_init = kwargs
        self.ids.constructor(args_init)
        self.run = CASE_RUN if args_init.get("run") is True else CASE_SKIP
        self.dependent = [x for x in str(args_init.get("dependent")).split(";") if args_init.get("dependent") is not None]
        self.dependent_var = [x for x in str(args_init.get("dependent_var")).split(";") if args_init.get("dependent_var") is not None]
        self.request.constructor(args_init)
        self.response.constructor(args_init)
        self.expect.constructor(args_init)
        self.sqlinfo.constructor(args_init)

    def bind_bench(self, bench_name):
        '''
        bind bench with bench_name
        :param bench_name:
        :return:
        '''
        self.bench_name = bench_name
        self.generate_log_key()

    def generate_log_key(self):
        '''
        generate log key to self
        :return:
        '''
        self.log_key = self.key = f"{self.bench_name}$%{self.ids.id}.{self.ids.subid}.{self.ids.name}$%"

    def deserialize(self):
        '''
        return dict type of api case
        :return:
        '''
        return {
            "ids": self.ids.deserialize(),
            "run": self.run,
            "dependent": self.dependent,
            "dependent_var" : self.dependent_var,
            "bench_name": self.bench_name,
            "request": self.request.deserialize(),
            "response": self.response.deserialize(),
            "expect": self.expect.deserialize(),
            "sqlinfo": self.sqlinfo.deserialize(),
            "type": self.type
        }


class AppCase(BaseCase):
    '''
    app case
    '''
    def __init__(self):
        super().__init__()
        self.mark = CASE_MARK_APP
        self.type = CASE_TYPE_APP
        self.message_type = MESSAGE_TYPE_CASE
        self.log_key = ""
        self._init_all()

    def _init_all(self):
        '''
        init all app case's needed
        :return:
        '''
        self.ids = AppIds()
        self.run = CASE_RUN
        self.dependent = []
        self.bench_name = ""
        self.stages = {}
        self.log_key = ""
        self.wait_activity = ""
        self.desired_caps = DesiredCaps()
        self.error = None
        self.sqlinfo = SqlInfo()
        self.time_sleep = 5
        self.pngs = {}

    def constructor(self, *args, **kwargs):
        '''
        :param args:
        :param kwargs:
        :return:
        '''
        args_init = {}
        if len(args) > 0 and isinstance(args[0], dict):
            args_init = args[0]
        else:
            args_init = kwargs
        self.ids.constructor(args_init)
        self.time_sleep = args_init.get("wait_time") or 5
        self.run = CASE_RUN if args_init.get("run") is True else CASE_SKIP
        self.dependent = [x for x in str(args_init.get("dependent")).split(";") if args_init.get("dependent") is not None]
        self.desired_caps.constructor(args_init.get("desired_caps"))
        self.stages = {}
        self.wait_activity = args_init.get("wait_activity", None)
        for s in args_init.get("stage"):
            stage = Stage()
            stage.constructor(s)
            self.stages[stage.id] = stage

    def bind_bench(self, bench_name):
        '''
        bind bench with bench name
        :param bench_name:
        :return:
        '''
        self.bench_name = bench_name
        self.generate_log_key()

    def generate_log_key(self):
        '''
        generate log key to self
        :return:
        '''
        self.log_key = self.key = f"{self.bench_name}$%{self.ids.id}.{self.ids.subid}.{self.ids.name}$%"

    def deserialize(self):
        '''
        return dict type of self
        :return:
        '''
        return {
            "ids": self.ids.deserialize(),
            "run": self.run,
            "dependent": self.dependent,
            "bench_name": self.bench_name,
            "stage": [stage.deserialize() for stage in self.stages.values()],
            "type": self.type,
            "desired_caps": self.desired_caps.deserialize(),
            "pngs": self.pngs,
            "sleep": self.time_sleep,
            "wait_activity": self.wait_activity
        }


class WebCase(BaseCase):
    '''
    web case
    '''
    def __init__(self):
        super().__init__()
        self.mark = CASE_MARK_WEB
        self.type = CASE_TYPE_WEBUI
        self.message_type = MESSAGE_TYPE_CASE
        self.log_key = ""
        self._init_all()

    def _init_all(self):
        '''
        init all web case's needed
        :return:
        '''
        self.ids = WebIds()
        self.run = CASE_RUN
        self.dependent = []
        self.bench_name = ""
        self.stages = {}
        self.log_key = ""
        self.wait_activity = ""
        self.desired_caps = WebDesiredCaps()
        self.error = None
        self.sqlinfo = SqlInfo()
        self.time_sleep = 5
        self.pngs = {}

    def constructor(self, *args, **kwargs):
        '''
        :param args:
        :param kwargs:
        :return:
        '''
        args_init = {}
        if len(args) > 0 and isinstance(args[0], dict):
            args_init = args[0]
        else:
            args_init = kwargs
        self.ids.constructor(args_init)
        self.time_sleep = args_init.get("wait_time") or 5
        self.run = CASE_RUN if args_init.get("run") is True else CASE_SKIP
        self.dependent = [x for x in str(args_init.get("dependent")).split(";") if args_init.get("dependent") is not None]
        self.desired_caps.constructor(args_init.get("desired_caps"))
        self.stages = {}
        self.wait_activity = args_init.get("wait_activity", None)
        for s in args_init.get("stage"):
            stage = WebStage()
            stage.constructor(s)
            self.stages[stage.id] = stage

    def bind_bench(self, bench_name):
        '''
        bind bench with bench name
        :param bench_name:
        :return:
        '''
        self.bench_name = bench_name
        self.generate_log_key()

    def generate_log_key(self):
        '''
        generate log key to self
        :return:
        '''
        self.log_key = self.key = f"{self.bench_name}$%{self.ids.id}.{self.ids.subid}.{self.ids.name}$%"

    def deserialize(self):
        '''
        return dict type of self
        :return:
        '''
        return {
            "ids": self.ids.deserialize(),
            "run": self.run,
            "dependent": self.dependent,
            "bench_name": self.bench_name,
            "stage": [stage.deserialize() for stage in self.stages.values()],
            "type": self.type,
            "desired_caps": self.desired_caps.deserialize(),
            "pngs": self.pngs,
            "sleep": self.time_sleep,
            "wait_activity": self.wait_activity
        }
