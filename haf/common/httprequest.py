# encoding='utf-8'

'''
file name : httpreqeust
description : http request all need this
others :
    support GET POST PUT DELETE method
    support with headers, data
'''


import json
import urllib.request as ur
import urllib.parse
import urllib.error as urlerror
from haf.common.log import Log
import traceback

logger = Log.getLogger(__name__)


class HttpController(object):
    '''
    HttpController
    using to the get/post/others
    '''

    def __init__(self):
        pass

    @staticmethod
    def getdata(data):
        '''
        getdata: using to make data to the url type

        :param data: the origin data
        :return the url type data
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
        get of http

        :param url the request url
        :param data the origin data
        :param headers the get headers

        :return the response of get
        '''
        key = kwargs.get("key")
        try:
            url = url + HttpController.getdata(data)
            logger.info(f'{key} [url] {url}', __name__)
            # using requests to Request the url with headers and method get
            request = ur.Request(url=url, headers=headers, method="GET")
            if headers is not None:
                for key in headers.keys():
                    request.add_header(key, headers[key])
            response = ur.urlopen(request, timeout=10)

            if response is None:
                return {"result": "None"}
            else:
                logger.info(f"{key} {str(response)}", __name__)

            return response
        except ur.URLError as e:
            logger.info(f"{key}{str(e)}", __name__)
            logger.info(f"{key}{traceback.format_exc()}", __name__)
            return e
        except Exception as ee:
            logger.info(f"{key}{str(ee)}")
            logger.info(f"{key}{traceback.format_exc()}", __name__)
            return ee

    @staticmethod
    def post(url, data=None, headers=None, **kwargs):
        '''
        post of http

        :param url the request url
        :param data the origin data
        :param headers the post headers

        :return the response of post
        '''
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
                logger.info(f"{key} {str(response)}", __name__)

            return response
        except ur.URLError as e:
            logger.error(f"{key} {str(e)}", __name__)
            return e
        except urlerror.HTTPError as httpe:
            logger.error(f"{key} { str(httpe)}", __name__)
            return httpe
        except Exception as ee:
            logger.error(f"{key} {str(ee)}", __name__)
            return ee

    def put(self, url, data=None, **kwargs):
        '''
        put of http

        :param url the request url
        :param data the origin data
        :param headers the put headers

        :return the response of put
        '''
        key = kwargs.get("key")
        try:
            data = bytes(data, encoding='utf8') if data is not None else None
            request = ur.Request(url, headers=self.headers, data=data)
            request.get_method = lambda: 'PUT'
            response = ur.urlopen(request, timeout=10)
            result = response.read()
            return result
        except ur.URLError as e:
            logger.error(f"{key} {str(e)}", __name__)
        except Exception as ee:
            logger.error(f"{key} {str(ee)}", __name__)

    def delete(self, url, data=None):
        '''
        delete of http

        :param url the request url
        :param data the origin data
        :param headers the delete headers

        :return the response of delete
        '''
        data = bytes(data, encoding='utf8') if data is not None else None
        try:
            request = ur.Request(url, headers=self.headers, data=data)
            request.get_method = lambda: 'DELETE'
            response = ur.urlopen(request, timeout=10)
            result = response.read()
            data = data.encode() if data is not None else None
            return result
        except ur.URLError as e:
            logger.error(str(e), __name__)
        except Exception as ee:
            logger.error(str(ee), __name__)
