# encoding='utf-8'
import sys


class BaseException(Exception):
    def __init__(self):
        self.exception = sys.exec_info()


class FailFrameworkException(BaseException):
    def __init__(self):
        pass


class FailAssertException(AssertionError):
    def __init__(self):
        pass


class FailLoaderException(BaseException):
    def __init__(self):
        pass


class FailRunnerException(BaseException):
    def __init__(self):
        pass


class FailRecorderException(BaseException):
    def __init__(self):
        pass


class FailCaseException(BaseException):
    def __init__(self):
        pass


class FailResultException(BaseException):
    def __init__(self):
        pass


class SkipCaseException(BaseException):
    def __init__(self):
        pass


class FailBusException(BaseException):
    def __init__(self):
        pass


class FailLoadCaseFromPyException(BaseException):
    def __init__(self):
        pass