#encoding='utf-8'

import sys

from haf.apihelper import Request

sys.path.append("..")
from haf.mark import test, skip, parameterize
from haf.case import BaseCase


class TestHello(BaseCase):
    request = Request()

    @test("test hello11")
    def test_1(self):
        assert 1+1 == 2
        assert 1 == 5

    @skip
    @test("test hello12")
    def test_2(self):
        assert 1 + 1 == 2

    @test
    @parameterize([{"test":123},{"test":245}])
    def test_3(self, params):
        print(params)
        assert 1 + 1 == 2

    @parameterize([{"test":123},{"test":245}])
    def test_4(self, params):
        assert params.get("test")==123


class TestHello2(BaseCase):
    @test("test hello2")
    def test1(self):
        self.request = Request()
        assert 1+1 == 2

    @test("test hello21")
    def test2(self):
        assert 1 + 1 == 2

