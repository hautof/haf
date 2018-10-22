import os,sys,time,datetime,json
import urllib.request as requests

from haf.pylib.Log.LogController import LogController

open_debug = True

class_name = "JsonTool"
logger = LogController.getLogger(class_name)

class JsonTool(object):
    '''
    Json 工具类 

    json 相关的操作 建议 添加到这里
    '''
    def __init__(self):
        pass
        self.class_name = "JsonTool"
        self.json_res = {}
        self.logtool = LogShow(self.class_name)

    def __str__(self):
        return self.class_name
    
    def getJson(self):
        return self.json_res

    def anaPostresult(self, result):
        if isinstance(result, requests.Request):
            if result.status_code == 200:
                return True
            else:
                return False

    def serialize(self, class_name, jsoninfo):
        if jsoninfo is None:
            return None
        try:
            if type(jsoninfo) != type({}):
                if open_debug:
                    self.logtool.log_print ("debug", str(class_name) + " -- " + str(jsoninfo), "serialize")
                json_result = json.loads(jsoninfo)
                if open_debug:
                    self.logtool.log_print ("debug", str(class_name) + " -- " + str(json_result), "serialize")
                return self.createClass(class_name, json_result)
            if type(jsoninfo) == type({}):
                return self.createClass(class_name, jsoninfo)
            # if type(jsoninfo) == type([]):
            #     return self.createClass(class_name, jsoninfo)
        except TypeError as e:
            print("[error][JsonTool-serialize] " + str(class_name) + " -- " + str(e))
            raise NoneTypeException
            #return self.createClass(class_name, jsoninfo)
        except ValueError as ee:
            return self.createClass(class_name, jsoninfo)

    def deserialize(self, cla):
        if cla is None:
            return None
        try:
            jsoninfo = self.getJsonfromClass(cla)
        except:
            jsoninfo = cla
        if jsoninfo is None:
            return None
        else:
            try:
                jsoninfo = json.dumps(jsoninfo)
            except:
                pass
        return jsoninfo
    
    def createClass(self, class_name, json_result):
        pass

    def getJsonfromClass(self, cla):        
        return cla.getJson()
    
    @staticmethod
    def Str2Json(strs):
        '''
        str to json 

        :参数:
        * strs :  要转化的数据

        :return: json对象
        '''
        try:
            #print(strs)
            if isinstance(strs, bytes):
                return json.loads(str(strs, encoding = "utf8"))
            else: 
                return json.loads(strs)
                
        except Exception as e:
            logger.log_print("error", e, "Str2Json")
            return strs

    @staticmethod
    def Str2List(strs, split):
        '''
        str to list, 将包含 split 标记的字符串 分割为 list

        :参数:

        * strs : 原始数据
        * split : 分隔符
        
        :return: list
        '''
        if isinstance(strs, list):
            return strs
        if not isinstance(strs, str) or not isinstance(split, str):
            return False
        try:
            tempstr = strs.split(split)
            for t in tempstr:
                t = t.strip()
            logger.log_print("info", tempstr, "Str2List")
            return tempstr
        except Exception as e:
            logger.log_print("error", e, "Str2Json")
            return strs
    
    @staticmethod
    def Json2List(jsons, ids):
        '''
        jsons to list with ids
        
        :args:

        * jsons * : json strs
        * ids * : id to list

        :return: list
        '''

        if isinstance(jsons, list):
            return jsons
        
        if not isinstance(jsons, dict) or not isinstance(ids, list):
            return False

    @staticmethod
    def Write2File(json, filename):
        '''
        write jsons to file

        :args: 

        * json * : json 
        * filename * : write to file
        '''
        try:
            f = open(filename, "w")
            f.writelines(str(json))
            f.close()
        except Exception as e:
            logger.log_print("error", e)