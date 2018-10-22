#encoding='utf-8'

import os, sys
import binascii
sys.path.append("../../..")
from haf.pylib.Log.LogController import LogController

logger = LogController.getLogger("methodsall")

class methodsall(object):
    @staticmethod
    def int(data):
        return int(data)

    @staticmethod
    def str(data):
        return str(data)
    
    @staticmethod
    def crc32(data):
        return  (binascii.crc32(bytes(str(data), encoding='utf-8')))

    @staticmethod
    def findTableIndex(tablename, rangeidx, data):
        tablename = str(tablename) 
        tablehashMap = {}
        tablehashRange = []

        for id in rangeidx:
            logger.log_print("debug", tablename + "_" + str(id))
            tablehash = methodsall.crc32(tablename + "_" + str(id))
            tablehashRange.append(tablehash)
            tablehashMap[str(tablehash)] = id
        
        data = methodsall.crc32(data)
        tablehashRange = sorted(tablehashRange)

        findhash = methodsall.findHashInRange(tablehashRange, data, 0)

        logger.log_print("debug", tablehashRange)
        logger.log_print("debug", tablehashMap)
        logger.log_print("debug", findhash)

        return tablehashMap.get(str(findhash))


    @staticmethod
    def findHashInRange(hashrange, data, id):
        find = None
        
        if len(hashrange) <= id:
            find = hashrange[0]
        else:
            logger.log_print("debug", str(id) + "---" + str(data) + " ?? " + str(hashrange[id]))
            if hashrange[id] < data:
                find = methodsall.findHashInRange(hashrange, data, id+1)
            else:
                find = hashrange[id]
            
        return find
    

if __name__ == "__main__":
    puid = 1325047
    tablename = "tbl_ques_result"
    rang = range(0,16)
    print(methodsall.findTableIndex(tablename, rang, puid))