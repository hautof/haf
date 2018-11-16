# encoding='utf-8'
from haf.apihelper import Request, Response, Ids, Expect
from haf.config import  *
from haf.result import BaseResult, HttpApiResult


class BaseCase(object):
    '''
    BaseCase the base of cases
    '''
    def __init__(self):
        self.name = None
        self.id = None
        self.subid = None
        self.type = None
        self.expect = None
        self.run = True
        self.AttrNoneList = ["result", "error", "AttrNoneList", ]


class HttpApiCase(BaseCase):
    def __init__(self):
        super().__init__()
        self.type = CASE_TYPE_BASE
        self.message_type = MESSAGE_TYPE_CASE
        self._init_all()

    def _init_all(self):
        self.ids = Ids()
        self.run = True
        self.request = Request()
        self.expect = Expect()
        self.response = Response()

    def constructor(self, *args, **kwargs):
        args_init = {}
        if len(args) > 0 and isinstance(args[0], dict):
            args_init = args[0]
        else:
            args_init = kwargs

        self.ids.constructor(args_init)
        self.run = args_init.get("run")
        self.request.constructor(args_init)
        self.response.constructor(args_init)
        self.expect.constructor(args_init)

