# encoding='utf-8'

from haf.pylib.Log.LogController import LogController
import haf.pylib.tools.globalvar as gl
from haf.pylib.tools.methodsall import methodsall

class_name = "TestCaseReplace"
logger = LogController.getLogger(class_name)


class TestCaseReplace(object):
    def switchDict(self, data):
        for key in data.keys():
            if data[key] is None:
                return data
            if "othercasezhan" in str(data[key]):
                if isinstance(data[key], str):
                    allstr = data[key].split("*othercasezhan*")
                    others = allstr[0]
                    allinfos = allstr[1].split("*")

                    method = getattr(methodsall, allinfos[0])
                    logger.log_print("debug", method)

                    id = allinfos[1]
                    subid = allinfos[2]
                    name = allinfos[3]
                    case = self.getTestCaseByIdSubidName(id, subid, name)
                    logger.log_print("debug", case)
                    key_endstr = getattr(case, allinfos[4])

                    for x in allinfos[5:]:
                        key_endstr = key_endstr[x]
                    if allinfos[0] == "int":
                        data[key] = method(key_endstr)
                    else:
                        data[key] = others + method(key_endstr)
                        
                elif isinstance(data[key], list):
                    data[key] = self.switchList(data[key])

        logger.log_print("info", "ok " + str(data))
        return data
    
    def switchList(self, data):
        if data is None:
            return data
        data_re = []
        for datax in data:
            if "othercasezhan" in str(datax):
                allstr = datax.split("*othercasezhan*")
                others = allstr[0]
                
                allinfos = allstr[1].split("*")

                method = getattr(methodsall, allinfos[0])

                logger.log_print("debug", method)

                id = allinfos[1]
                subid = allinfos[2]
                name = allinfos[3]
                case = self.getTestCaseByIdSubidName(id, subid, name)
                logger.log_print("debug", case)
                key_endstr = getattr(case, allinfos[4])

                for x in allinfos[5:]:
                    key_endstr = key_endstr[x]
                if allinfos[0] == "int":
                    data_re.append(others + str(method(key_endstr)))
                else:
                    data_re.append(others + key_endstr)
            elif "findtableid" in str(datax):
                allstr = datax.split("*findtableid*")
                others = allstr[0]
                othersend = allstr[2]

                allinfos = allstr[1].split("*")

                method = getattr(methodsall, allinfos[0])
                logger.log_print("debug", method)

                datastr = allinfos[1]
                rang_start = allinfos[2]
                rang_end = allinfos[3]
                tablename = allinfos[4]

                datax =  str(method(tablename, range(int(rang_start),int(rang_end)), datastr))

                data_re.append(others + datax + othersend)

            else:
                data_re.append(datax)
        logger.log_print("info", "ok {}".format(str(data_re)))
        return data_re

    def switch(self, data):
        logger.log_print("info", "start {}".format(str(data)))
        if isinstance(data, dict):
            return self.switchDict(data)
        elif isinstance(data, list):
            return self.switchList(data)
        else :
            return data

    def getTestCaseByIdSubidName(self, id, subid, name):
        logger.log_print("info", "start {}-{}-{}".format(str(id), str(subid), str(name)))
        testcases = gl.get_value("testcases")
        for case in testcases:
            logger.log_print("debug", str(case.id) + "-" + str(case.subid) + "-" + str(case.name))
            if str(case.id) == str(id) and str(case.subid) == str(subid) and ((str(case.name) in str(name)) or (str(name) in str(case.name))):
                logger.log_print("debug",  "OK" )
                return case
        return None

