# encoding='utf-8'
from datetime import datetime

from assertpy import assert_that
from haf.common.log import Log
from deepdiff import DeepDiff
logger = Log.getLogger(__name__)


class AssertHelper(object):
    @staticmethod
    def assert_that(real, expect, **kwargs):
        key = kwargs.get("key", "assert$%test$%")
        try:
            logger.debug(f"{key} {DeepDiff(real, expect, ignore_order=True)}")
            logger.debug(f"{key} {real} ?? {expect}")
            if real is None or expect is None:
                return real == expect
            elif isinstance(real, datetime):
                expect = datetime.strptime(expect, "%Y-%m-%d %H:%M:%S")
                return AssertHelper.check_datetime(real, expect)
            elif isinstance(real, dict) and isinstance(expect, dict):
                result = True
                for temp in real.keys():
                    result = result and AssertHelper.assert_that(real.get(temp), expect.get(temp))
                return result
            elif isinstance(real, list) and isinstance(expect, list):
                result = True
                for temp_real in real:
                    result = result and temp_real in expect
                for temp_expect in expect:
                    result = result and temp_expect in real
                return result
            else:
                assert_that(type(real)(expect)).is_equal_to(real)
                return type(real)(expect) == real
        except AssertionError as ae:
            logger.debug(f"{key} {ae}")
            return ae

    @staticmethod
    def check_datetime(real, expect):
        l = ['year', 'month', 'day', 'hour', 'minute', 'second']
        for x in l:
            if getattr(real, x) == getattr(expect, x):
                continue
            else:
                return False
        return True
