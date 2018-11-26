# encoding='utf-8'

import json
import urllib.request as ur
import urllib.parse
import urllib.error as urlerror
from haf.common.log import Log
import traceback

logger = Log.getLogger(__name__)

class HttpController(object):
    '''
    Http 请求 管理类
    '''

    def __init__(self):
        pass

    @staticmethod
    def getdata(data):
        '''
        将 get 的 data 格式化为 url 参数 形式

        :参数:
        * data : str/bytes/dict get 请求的参数
        :return: data
        '''
        datastr = "?"
        if isinstance(data, bytes):
            data = str(data, encoding="utf-8")
        if isinstance(data, str):
            try:
                data = json.loads(data)
                for d in data.keys():
                    datastr = datastr + str(d) + "=" + str(data[d]) + "&"
            except:
                return data
        elif isinstance(data, dict):
            for d in data.keys():
                datastr = datastr + str(d) + "=" + str(data[d]) + "&"

        return datastr[:-1]  # delete & at the last position

    @staticmethod
    def get(url, data=None, headers=None, **kwargs):
        '''
        http get 请求方法
        :参数:
        * url : 请求的 url
        :return: response.read() 返回的 请求内容
        '''
        key = kwargs.get("key")
        try:
            url = url + HttpController.getdata(data)
            logger.info(f'{key} [url] {url}')
            request = ur.Request(url=url, headers=headers, method="GET")
            if headers is not None:
                for key in headers.keys():
                    request.add_header(key, headers[key])
            response = ur.urlopen(request, timeout=10)

            if response is None:
                return {"result": "None"}
            else:
                logger.info(f"{key} {str(response)}")

            return response
        except ur.URLError as e:
            logger.info(f"{key}{str(e)}")
            logger.info(f"{key}{traceback.format_exc()}")
            traceback.print_exc()
            return e
        except Exception as ee:
            traceback.print_exc()
            logger.info(f"{key}{str(ee)}")
            logger.info(f"{key}{traceback.format_exc()}")
            return ee

    @staticmethod
    def post(url, data=None, headers=None, **kwargs):
        key = kwargs.get("key")
        try:
            if "application/json" in headers.values():
                data = bytes(json.dumps(data), encoding='utf-8')
            else:
                data = bytes(urllib.parse.urlencode(data), encoding='utf-8')

            request = ur.Request(url=url, data=data, headers=headers, method="POST")
            response = ur.urlopen(request)

            if response is None:
                return {"result": "None"}
            else:
                logger.info(f"{key} {str(response)}")

            return response
        except ur.URLError as e:
            logger.error(f"{key} {str(e)}")
            traceback.print_exc()
            return e
        except urlerror.HTTPError as httpe:
            logger.error(f"{key} { str(httpe)}")
            traceback.print_exc()
            return httpe
        except Exception as ee:
            logger.error(f"{key} {str(ee)}")
            traceback.print_exc()
            return ee

    def put(self, url, data=None, **kwargs):
        key = kwargs.get("key")
        try:
            data = bytes(data, encoding='utf8') if data is not None else None
            request = ur.Request(url, headers=self.headers, data=data)
            request.get_method = lambda: 'PUT'
            response = ur.urlopen(request, timeout=10)
            result = response.read()
            return result
        except ur.URLError as e:
            traceback.print_exc()
            logger.error(f"{key} {str(e)}")
        except Exception as ee:
            traceback.print_exc()
            logger.error(f"{key} {str(ee)}")

    def delete(self, url, data=None):
        data = bytes(data, encoding='utf8') if data is not None else None
        try:
            request = ur.Request(url, headers=self.headers, data=data)
            request.get_method = lambda: 'DELETE'
            response = ur.urlopen(request, timeout=10)
            result = response.read()
            data = data.encode() if data is not None else None
            return result
        except ur.URLError as e:
            logger.error(str(e))
        except Exception as ee:
            logger.error(str(ee))
