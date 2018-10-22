import os,time,datetime,json,sys,threading
import urllib.request as ur
import urllib.parse
import urllib.error as urlerror
import urllib3
from http.cookiejar import CookieJar
sys.path.append("../../../")
from haf.pylib.Log.LogController import LogController
open_debug = True

class_name = "HttpController"
logger = LogController.getLogger(class_name)
headers = {}
headers["Accept"] = "application/json"


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
        
        return datastr[:-1] #delete & at the last position

    @staticmethod
    def get(url, data=None, headers=None):
        '''
        http get 请求方法
        :参数:
        * url : 请求的 url

        :return: response.read() 返回的 请求内容
        '''
        try:
            url=url+HttpController.getdata(data)            
            
            logger.log_print("debug", '[url] ' + url, "get")
            request = None
            response = None
            result = None
            
            #data = bytes(urllib.parse.urlencode(data), encoding='utf-8')    
            request = ur.Request(url=url, headers=headers, method="GET") 
            if headers is not None:
                #headers = bytes(urllib.parse.urlencode(headers), encoding='utf-8')
                for key in headers.keys():
                    request.add_header(key, headers[key])
            response = ur.urlopen(request)
            
            
            #if isinstance(result, bytes):
            #    result = str(result, encoding="utf-8")
            if open_debug:
                logger.log_print("debug", str(response), "get")
            if response is None:
                return {"result":"None"}
            else:
                logger.log_print("debug", str(response), "get-response")

            return response
        except ur.URLError as e:
            logger.log_print ("error", str(e), "get")
            return e
        except Exception as ee:
            logger.log_print ("error", str(ee), "get")

    @staticmethod
    def post(url, data=None, headers=None, **kwargs):
        try:
            if open_debug:
                logger.log_print("debug", '[url] ' + url, "post")
            
            request = None
            response = None
            result = None
            
            if "application/json" in headers.values():
                data = bytes(json.dumps(data), encoding='utf-8')
            else:
                data = bytes(urllib.parse.urlencode(data), encoding='utf-8')    
            
            request = ur.Request(url=url, data=data, headers=headers, method="POST") 
            response = ur.urlopen(request)
            
            #if isinstance(result, bytes):
            #    result = str(result, encoding="utf-8")
            if open_debug:
                logger.log_print("debug", str(response), "post")
            if response is None:
                return {"result":"None"}
            else:
                logger.log_print("debug", str(response), "post-resposne")

            return response
        except ur.URLError as e:
            logger.log_print ("error", str(e), "post")
            if e.code == 400 or e.code == 404:
                return e
        except urlerror.HTTPError as httpe:
            logger.log_print("error", str(httpe), "post-httperror")
            if httpe.code == 400:
                return httpe
        except Exception as ee:
            logger.log_print ("error", str(ee), "post")

    def put(self, url, data=None):
        try:  
            if open_debug:
                logger.log_print("debug", '[url] ' + url, "put")
            request = None
            response = None
            result = None
            data = bytes(data, encoding='utf8')  if data is not None else None
            request = ur.Request(url, headers=self.headers, data=data)
            request.get_method = lambda: 'PUT'
            response = ur.urlopen(request, timeout=10)
            result = response.read()
            if open_debug:
                logger.log_print("debug", 'put = ' + str(result), "put")
            return result
        except ur.URLError as e:
            logger.log_print ("error", str(e), "put")
        except Exception as ee:            
            logger.log_print ("error", str(ee), "put")
            raise NoneTypeException
        
    def delete(self, url, data=None):
        data = bytes(data, encoding='utf8')  if data is not None else None
        try:
            if open_debug:
                logger.log_print("debug", '[url] ' + url, "delete")
            request, response, result = None, None, None
            request = ur.Request(url, headers=self.headers, data=data)
            request.get_method = lambda:'DELETE'   
            response = ur.urlopen(request, timeout=10)
            result = response.read()
            data = data.encode() if data is not None else None
            if open_debug:
                logger.log_print("debug", "delete = " + str(result), "delete")
            return result
        except ur.URLError as e:
            logger.log_print("error", str(e), "delete")
        except Exception as ee:
            logger.log_print("error", str(ee), "delete")
            raise NoneTypeException

    def anaPostresult(self, result):
        return self.jsontool.anaPostresult(result)

    def serialize(self, class_name, jsoninfo):
        return self.jsontool.serialize(class_name, jsoninfo)

    def deserialize(self, cla):
        return self.jsontool.deserialize(cla)

    def getJsonfromClass(self, cla):        
        return self.jsontool.getJsonfromClass(cla)


if __name__ == "__main__":
    try:
        hc = HttpController()
        r = hc.post(url="http://api-server-corpus.zhan.com/toefl-ques/get-topic-avg-count?debug=1", data={"app_id": "beikao", "btype": 1,"topic_ids":[1,2]}, headers={"content-type":"application/json"})
        print(r.read())
        r = ur.urlopen(url="http://api-server-corpus.zhan.com/toefl-ques/get-topic-avg-count?debug=1", data=bytes('{"app_id": "beikao", "btype": 1,"topic_ids":[1,2]}',encoding='utf-8'))
        print(r.read())

    except ur.HTTPError as he:
        print(he.code)
    