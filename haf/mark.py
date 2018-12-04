# encoding='utf-8'
import functools
import inspect
from haf.case import PyCase


class TestDecorator:
    def __init__(self, func):
        self.func = func
        self.run = True
        self.reason = ""
        self.param = ""

    def __call__(self, param):
        self.param = param
        if len(self.param) > 0:
            return self.func(self, self.param)
        else:
            return self.func(self)


test = TestDecorator


class SkipDecorator:
    def __init__(self, test_item: test=None):
        self.test_item = test_item
        self.test_item.run = False

    def __call__(self):
        return self.test_item


skip = SkipDecorator


class ParametersDecorator:
    def __init__(self,  params: list=[]):
        self.params = params

    def __call__(self, *args, **kwargs):
        return self.params


parameters = ParametersDecorator
