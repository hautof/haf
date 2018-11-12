# encoding = utf-8


import haf.pylib.tools.globalvar as gl

from haf.pylib.Log.LogController import LogController

logger = LogController.getLogger(__name__)


class TestResult(object):
    def __init__(self):
        self.start_time = None
        self.finish_time = None
        