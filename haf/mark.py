# encoding='utf-8'


class TestDecorator:
    def __init__(self, func):
        self.func = func

    def __call__(self):
        pass


test = TestDecorator




