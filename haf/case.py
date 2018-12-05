# encoding='utf-8'
from haf.apihelper import Request, Response, Ids, Expect, SqlInfo
from haf.config import *
from haf.common.log import Log

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

    def bind_bench(self, bench_name):
        self.bench_name = bench_name
        self.generate_log_key()

    def generate_log_key(self):
        self.log_key = self.key = f"{self.bench_name}$%{self.ids.id}.{self.ids.subid}.{self.ids.name}$%"

    def deserialize(self):
        return {
            "ids": self.ids.deserialize(),
            "run": self.run,
            "bench_name": self.bench_name,
            "func": str(self.func),
            "type": self.type
        }


class HttpApiCase(BaseCase):
    def __init__(self):
        super().__init__()
        self.mark = CASE_MARK_API
        self.type = CASE_TYPE_HTTPAPI
        self.message_type = MESSAGE_TYPE_CASE
        self.log_key = ""
        self._init_all()

    def _init_all(self):
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
        self.dependent = [x for x in str(args_init.get("dependent")).split(";") if args_init.get("dependent") is not None]
        self.request.constructor(args_init)
        self.response.constructor(args_init)
        self.expect.constructor(args_init)
        self.sqlinfo.constructor(args_init)

    def bind_bench(self, bench_name):
        self.bench_name = bench_name
        self.generate_log_key()

    def generate_log_key(self):
        self.log_key = self.key = f"{self.bench_name}$%{self.ids.id}.{self.ids.subid}.{self.ids.name}$%"

    def deserialize(self):
        return {
            "ids": self.ids.deserialize(),
            "run": self.run,
            "dependent": self.dependent,
            "bench_name": self.bench_name,
            "request": self.request.deserialize(),
            "response": self.response.deserialize(),
            "expect": self.expect.deserialize(),
            "sqlinfo": self.sqlinfo.deserialize(),
            "type": self.type
        }