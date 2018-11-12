# encoding = utf-8


import haf.pylib.tools.globalvar as gl

from haf.pylib.Log.LogController import LogController
from haf.testcase.TestCase_ import TestCase_

logger = LogController.getLogger(__name__)


class TestSuite(object):

    def __init__(self):
        self.test_cases = []
        self.name = ""


    def append_case(self, testcase:TestCase_):
        self.test_cases.append(testcase)

    def append_cases(self, testcases:list):
        self.test_cases = testcases

    @property
    def case_count(self):
        return len(self.test_cases)

    @property
    def pass_count(self):
        count = 0
        for case in self.test_cases:
            if case.result:
                count += 1
        return count

    @property
    def fail_count(self):
        count = 0
        for case in self.test_cases:
            if not case.result:
                count += 1
        return count

    @property
    def skip_count(self):
        count = 0
        for case in self.test_cases:
            if not case.run:
                count += 1
        return count

    @property
    def error_count(self):
        count = 0
        for case in self.test_cases:
            pass
        return count

