#encoding='utf-8'

import sys
import time
from datetime import datetime

from haf.apihelper import Request

sys.path.append("..")
from haf.mark import test, skip, parameterize
from haf.case import BaseCase
from haf.utils import Utils


class TestHello(BaseCase):
    request = Request()

    @parameterize([{i:i} for i in range(10000)])
    def test_1(self, params):
        print(f"[{params}]start at", datetime.now().strftime("%H:%M:%S"))
        time_begin = datetime.now()
        print(params)
        data_request = {
            "request_header": {},
            "request_data": {},
            "method": "get",
            "host_port": "www.baidu.com",
            # "url": "/v1/front/keng/?building_id=2&location_id=1"
            "url": ""
        }
        time_temp = datetime.now()
        print(f"1:{datetime.now()-time_begin}")
        self.request.constructor(data_request)
        self.response = Utils.http_request(self.request)
        print(f"2:{datetime.now()-time_temp}")
        assert self.response.code == 200
        print(f"[{params}]end at", datetime.now().strftime("%H:%M:%S"))
        print(f"{datetime.now()-time_begin}")
