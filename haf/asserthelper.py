# encoding='utf-8'
from datetime import datetime

from assertpy import assert_that
from haf.common.log import Log

logger = Log.getLogger(__name__)


class AssertHelper(object):
    @staticmethod
    def assert_that(real, expect):
        #logger.debug("{} ?? {}".format(real, expect))
        if real is None or expect is None:
            return real == expect
        elif isinstance(real, datetime):
            try:
                expect = datetime.strptime(expect, "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                print(e)
            return AssertHelper.check_datetime(real, expect)
        elif isinstance(real, dict) and isinstance(expect, dict):
            try:
                result = True
                for temp in real.keys():
                    result = result and AssertHelper.assert_that(real.get(temp), expect.get(temp))
            except Exception as e:
                print(e)
            return result
        else:
            assert_that(type(real)(expect)).is_equal_to(real)
            return type(real)(expect) == real

    @staticmethod
    def check_datetime(real, expect):
        l = ['year', 'month', 'day', 'hour', 'minute', 'second']
        for x in l:
            if getattr(real, x) == getattr(expect, x):
                continue
            else:
                return False
        return True
