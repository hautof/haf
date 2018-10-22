# encoding='utf-8'


from haf.pylib.Log.LogController import LogController
from haf.check.CheckSQLGet import CheckSQLGet

logger = LogController.getLogger("corpus-checksql")


class sqlcheck(object):
    '''
    corpus SQL check third libs writen by third users
    '''

    @staticmethod
    def sqlcheck1(sqlresult, responseresult, sqlgetlist, **kwargs):
        '''
        检查 字典 类型，字典 data 是 list({})
        '''
        funcname = "sqlcheck1"
        
        logger.log_print("debug", "===========================================================>", funcname)
        logger.log_print("debug", sqlresult, funcname)
        logger.log_print("debug", responseresult, funcname)
        logger.log_print("debug", sqlgetlist, funcname)
        
        id = kwargs["id"]

        
        if "dataofown" in kwargs:
            dataup = responseresult
        else:
            dataup = responseresult["data"]
            if "dataother" in kwargs:
                dataup = dataup[kwargs["dataother"]]
        result = False
        for ls in sqlresult:
            result = False
            logger.log_print("debug", "ls = " + str(ls), funcname)
            
            for data in dataup:
                if isinstance(id, str):
                    if str(data[id]) == str(ls[0]):
                        i = 0
                        for l in ls:
                            if "exclude" in kwargs and sqlgetlist[i] in kwargs["exclude"]:
                                i += 1
                                continue
                            logger.log_print("debug",("@", sqlgetlist[i], "@ >> ", str(data.get(sqlgetlist[i])), " ?? ",str(l) ))
                            assert CheckSQLGet.Check(l, data.get(sqlgetlist[i])) is True
                            result = True
                            i += 1                        
                        break
                elif isinstance(id, list): # 多参数需要相同
                    checkid = True
                    for d,order in id:
                        if str(data[d]) == str(ls[order]):
                            continue
                        else:
                            checkid = False
                    if checkid:
                        i = 0
                        for l in ls:
                            if "exclude" in kwargs and sqlgetlist[i] in kwargs["exclude"]:
                                i += 1
                                continue
                            logger.log_print("debug", "@" + sqlgetlist[i] + "@ >> " + str(data.get(sqlgetlist[i])) + " ?? " + str(l) )
                            assert CheckSQLGet.Check(l, data.get(sqlgetlist[i])) is True
                            result = True
                            i += 1                        
                        break

        assert result==True
        logger.log_print("debug", "--------------------------------------------", funcname)
        for data in dataup:
            logger.log_print("debug", data)
            result = False
            for ls in sqlresult:
                if isinstance(id, str):
                    if str(data[id]) == str(ls[0]):
                        i = 0
                        for l in ls:
                            if "exclude" in kwargs and sqlgetlist[i] in kwargs["exclude"]:
                                i += 1
                                continue
                            logger.log_print("debug", "@" + sqlgetlist[i] + "@ >> " + str(data.get(sqlgetlist[i])) + " ?? " + str(l) )
                            assert CheckSQLGet.Check(l, data.get(sqlgetlist[i])) is True
                            i += 1  
                        result = True                      
                        break
                elif isinstance(id, list):
                    checkid = True
                    for d,order in id:
                        if str(data[d]) == str(ls[order]):
                            continue
                        else:
                            checkid = False
                    if checkid:
                        i = 0
                        for l in ls:
                            if "exclude" in kwargs and sqlgetlist[i] in kwargs["exclude"]:
                                i += 1
                                continue
                            logger.log_print("debug", "@" + sqlgetlist[i] + "@ >> " + str(data.get(sqlgetlist[i])) + " ?? " + str(l) )
                            assert CheckSQLGet.Check(l, data.get(sqlgetlist[i])) is True
                            i += 1  
                        result = True                      
                        break

        logger.log_print("debug", "debug for result=" + str(result))
        
        logger.log_print("debug", "<===========================================================", funcname)
        return result
        
    @staticmethod
    def sqlcheck2(sqlresult, responseresult, sqlgetlist, **kwargs):
        '''
        检查 字典 类型，字典 data values 中 无复杂类型
        '''
        funcname = "sqlcheck2"
            
        logger.log_print("debug", "===========================================================>", funcname)
        logger.log_print("debug", sqlresult, funcname)
        logger.log_print("debug", responseresult, funcname)
        logger.log_print("debug", sqlgetlist, funcname)
        
        result = False
        ls = sqlresult
        logger.log_print("debug", ls)
        if "id" not in kwargs:
            data = responseresult["data"]
        elif "id" in kwargs:
            data = responseresult

        i = 0
        for x in sqlgetlist:
            logger.log_print("debug","@" + x + "@ >> " + str(data.get(x)) + " ?? " + str(ls[i]) )
            assert CheckSQLGet.Check(ls[i], data.get(x)) is True
            result = True
            i += 1 
        assert result==True
        logger.log_print("debug", "--------------------------------------------", funcname)
        i = 0
        for x in sqlgetlist:
            logger.log_print("debug", "@" + x + "@ >> " + str(data.get(x)) + " ?? " + str(ls[i]) )
            assert CheckSQLGet.Check(ls[i], data.get(x)) is True
            result = True   
            i += 1
        logger.log_print("debug", "debug for result=" + str(result))
        logger.log_print("debug", "<===========================================================", funcname)
        assert result is True
        return result

    @staticmethod
    def sqlcheck3(sqlresult, responseresult, sqlgetlist, **kwargs):
        '''
        检查 字典 类型，字典 values 中 无复杂类型
        '''
        funcname = "sqlcheck3"
        logger.log_print("debug", "===========================================================>", funcname)
            
        logger.log_print("debug", sqlresult, funcname)
        logger.log_print("debug", responseresult, funcname)
        logger.log_print("debug", sqlgetlist, funcname)
        
        result = False
        ls = sqlresult
        logger.log_print("debug", ls)
        data = responseresult
        i = 0
        for x in sqlgetlist:
            logger.log_print("debug", "@" + x + "@ >> " + str(data.get(x)) + " ?? " + str(ls[i]) )
            assert CheckSQLGet.Check(ls[i], data.get(x)) is True
            result = True
            i += 1 
        assert result==True
        logger.log_print("debug", "------------------------------------------------------------------")
        i = 0
        for x in sqlgetlist:
            logger.log_print("debug", "@" + x + "@ >> " + str(data.get(x)) + " ?? " + str(ls[i]) )
            assert CheckSQLGet.Check(ls[i], data.get(x)) is True
            result = True   
            i += 1
        logger.log_print("debug", "debug for result=" + str(result))
        logger.log_print("debug", "<===========================================================", funcname)
        assert result is True
        return result

    @staticmethod
    def ShaiXuanShiJuanCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        return sqlcheck.sqlcheck1(sqlresult[0], responseresult, sqlgetlist, id="paperID")
            
    @staticmethod
    def HuoQuShiJuan(sqlresult, responseresult, sqlgetlist, **kwargs):
        logger.log_print("debug", "===========================================================>")
        logger.log_print("debug", sqlresult)
        logger.log_print("debug", responseresult)
        logger.log_print("debug", sqlgetlist)
        result = True
        for ls in sqlresult[0]:
            for tpo_group in responseresult["data"]["tpo_list"].values():
                break_check = False
                for data in tpo_group:
                    if str(data["paperID"]) == str(ls[0]):
                        i = 0
                        for l in ls:
                            logger.log_print("debug","@" + sqlgetlist[i] + "@ >> " + str(data.get(sqlgetlist[i])) + " ?? " + str(l) )
                            assert CheckSQLGet.Check(l, data.get(sqlgetlist[i]))
                            i += 1                        
                        break_check = True
                        break
                if break_check:
                    break
            for tpo_group in responseresult["data"]["extra_list"].values():
                break_check = False
                for data in tpo_group:
                    if str(data["paperID"]) == str(ls[0]):
                        i = 0
                        for l in ls:
                            logger.log_print("debug","@" + sqlgetlist[i] + "@ >> " +  str(data.get(sqlgetlist[i])) + " ?? " + str(l) )
                            assert CheckSQLGet.Check(l, data.get(sqlgetlist[i]))
                            i += 1                        
                        break_check = True
                        break
                if break_check:
                    break

        for tpo_group in responseresult["data"]["tpo_list"].values():
            for data in tpo_group:
                result = False
                for ls in sqlresult[0]:
                    if str(data["paperID"]) == str(ls[0]):
                        i = 0
                        for l in ls:
                            logger.log_print("debug","@" + sqlgetlist[i] + "@ >> " + str(data.get(sqlgetlist[i])) + " ?? " + str(l) )
                            assert CheckSQLGet.Check(l, data.get(sqlgetlist[i]))
                            i += 1  
                        result = True                      
                        break
                assert result
        for tpo_group in responseresult["data"]["extra_list"].values():
            for data in tpo_group:
                result = False
                for ls in sqlresult[0]:
                    if str(data["paperID"]) == str(ls[0]):
                        i = 0
                        for l in ls:
                            logger.log_print("debug","@" + sqlgetlist[i] + "@ >> " + str(data.get(sqlgetlist[i])) + " ?? " + str(l) )
                            assert CheckSQLGet.Check(l, data.get(sqlgetlist[i]))
                            i += 1  
                        result = True                      
                        break
                assert result
        logger.log_print("debug", "<===========================================================")
        return True

    @staticmethod
    def HuoQuWenZhangXiangQingCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        return sqlcheck.sqlcheck2(sqlresult[0][0], responseresult, sqlgetlist)

    @staticmethod
    def HuoQuWenZhangTiMuCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        return sqlcheck.sqlcheck1(sqlresult[0], responseresult, sqlgetlist, id="questionID")
        
        
    @staticmethod
    def HuoQUTiMuTiXingCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        logger.log_print("debug", "===========================================================>")
        logger.log_print("debug", sqlresult)
        logger.log_print("debug", responseresult)
        logger.log_print("debug", sqlgetlist)
        result = True
        for ls in sqlresult[0]:
            for data in responseresult["data"]:
                if str(data["questionID"]) == str(ls[0]):
                    i = 0
                    for l in ls:
                        if str(sqlgetlist[i]) in ["difficulty", "seqno"]:
                            i += 1
                            continue
                        if "paragraphDetail" in str(sqlgetlist[i]) or "translation" in str(sqlgetlist[i]):
                            logger.log_print("debug", l)
                            l = l.replace('<m_p>', '<m_p><m_s>').replace('@@@@', '</m_s><m_s>').replace('</m_p>', '</m_s></m_p>')
                            logger.log_print("debug", l)
                        logger.log_print("debug", "@" + sqlgetlist[i] + "@ >> " + str(data.get(sqlgetlist[i])) + " ?? " + str(l) )
                        assert CheckSQLGet.Check(l, data.get(sqlgetlist[i]))
                        i += 1                        
                    break

        for data in responseresult["data"]:
            result = False
            for ls in sqlresult[0]:
                if str(data["questionID"]) == str(ls[0]):
                    i = 0
                    for l in ls:
                        if str(sqlgetlist[i]) in ["difficulty", "seqno"]:
                            i += 1
                            continue
                        if "paragraphDetail" in str(sqlgetlist[i]) or "translation" in str(sqlgetlist[i]):
                            logger.log_print("debug", l)
                            l = l.replace('<m_p>', '<m_p><m_s>').replace('@@@@', '</m_s><m_s>').replace('</m_p>', '</m_s></m_p>')
                            logger.log_print("debug", l)
                        logger.log_print("debug", "@" + sqlgetlist[i] + "@ >> " +str(data.get(sqlgetlist[i])) + " ?? " + str(l) )
                        assert CheckSQLGet.Check(l, data.get(sqlgetlist[i]))
                        i += 1  
                    result = True                      
                    break
            assert result
        logger.log_print("debug", "<===========================================================")
        return True
    
    @staticmethod
    def HuoQuTiMuLeiXingLieBiaoCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        return sqlcheck.sqlcheck1(sqlresult[0], responseresult, sqlgetlist, id="id", **kwargs)

    @staticmethod
    def GetQuesByTopicidCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        return sqlcheck.sqlcheck1(sqlresult[0], responseresult, sqlgetlist, id=[["questionID",2]], exclude=["relatedParagraph"],**kwargs)

    @staticmethod
    def TuoFuCuoTiBangCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        logger.log_print("debug", "===========================================================>")
        logger.log_print("debug", sqlresult, "TuoFuCuoTiBangCheck")
        logger.log_print("debug", responseresult, "TuoFuCuoTiBangCheck")
        logger.log_print("debug", sqlgetlist, "TuoFuCuoTiBangCheck")
        try:
            result = False
            for ls in sqlresult[0]:
                result = False
                logger.log_print("debug", ls)
                for data in responseresult["data"]:
                    if str(data["topic_id"]) == str(ls[0]):
                        i = 0
                        for l in ls:
                            if "ranking" in sqlgetlist[i]:
                                continue
                            logger.log_print("debug","@" + sqlgetlist[i] + "@ >> " + str(data.get(sqlgetlist[i])) + " ?? " + str(l) )
                            assert CheckSQLGet.Check(l, data.get(sqlgetlist[i])) is True
                            result = True
                            i += 1                        
                        break
            assert result==True

            for data in responseresult["data"]:
                logger.log_print("debug", data)
                result = False
                for ls in sqlresult[0]:
                    if str(data["topic_id"]) == str(ls[0]):
                        i = 0
                        for l in ls:
                            if "ranking" in sqlgetlist[i]:
                                continue
                            logger.log_print("debug","@" + sqlgetlist[i] + "@ >> " + str(data.get(sqlgetlist[i])) + " ?? " + str(l) )
                            assert CheckSQLGet.Check(l, data.get(sqlgetlist[i])) is True
                            i += 1  
                        result = True                      
                        break
            logger.log_print("debug", "debug for result".format(str(result)))
            assert result is True
            logger.log_print("debug", "<===========================================================")
        finally:
            return result

    @staticmethod
    def HuoQuTiMuLianXiTongJiCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        return sqlcheck.sqlcheck1(sqlresult[0], responseresult, sqlgetlist, id="topic_id")

    @staticmethod
    def HuoQuGeJiFenLeiBiaoQianCheck(sqlresult, responseresult, sqlgetlist, others=None, **kwargs):
        logger.log_print("debug", "===========================================================>")
        logger.log_print("debug", sqlresult, "HuoQuGeJiFenLeiBiaoQianCheck")
        logger.log_print("debug", responseresult, "HuoQuGeJiFenLeiBiaoQianCheck")
        logger.log_print("debug", sqlgetlist, "HuoQuGeJiFenLeiBiaoQianCheck")
        default_name = "subject_classify"
        if others is not None:
            default_name = others
        result = False
        j = 1
        for lss in sqlresult:
            for data in responseresult["data"][default_name]["child"]:
                if str(data["value"]) == str(j):
                    for ls in lss:
                        result = False
                        logger.log_print("debug", ls, "HuoQuGeJiFenLeiBiaoQianCheck")
                        for x in data["child"]:
                            if str(x.get("id")) == str(ls[0]):
                                logger.log_print("debug", x, "HuoQuGeJiFenLeiBiaoQianCheck")
                                i = 0
                                for s in sqlgetlist:
                                    logger.log_print("debug","@" + s + "@ >> " + str(x.get(s)) + " ?? " + str(ls[i]), "HuoQuGeJiFenLeiBiaoQianCheck" )
                                    assert CheckSQLGet.Check(ls[i], x.get(s)) is True
                                    result = True    
                                    i += 1     
                                break
                    assert result==True
            j += 1
        

        result = False
        for data in responseresult["data"][default_name]["child"]:
            j = 1
            for lss in sqlresult:
                if str(data["value"]) == str(j):
                    for x in data["child"]:
                        result = False
                        logger.log_print("debug", ls, "HuoQuGeJiFenLeiBiaoQianCheck")
                        for ls in lss:
                            if str(x.get("id")) == str(ls[0]):
                                logger.log_print("debug", x, "HuoQuGeJiFenLeiBiaoQianCheck")
                                i = 0
                                for s in sqlgetlist:
                                    logger.log_print("debug","@" + s + "@ >> " +str(x.get(s)) + " ?? " + str(ls[i]) , "HuoQuGeJiFenLeiBiaoQianCheck")
                                    assert CheckSQLGet.Check(ls[i], x.get(s)) is True
                                    i += 1     
                                result = True 
                                break
                            
                    assert result==True
                j += 1
        
        logger.log_print("debug", "<===========================================================")
        return result
    
    @staticmethod
    def HuoQuGeJiFenLeiBiaoQianChecklisten(sqlresult, responseresult, sqlgetlist, **kwargs):
        logger.log_print("debug", "===========================================================>")
        logger.log_print("debug", sqlresult, "HuoQuGeJiFenLeiBiaoQianChecklisten")
        logger.log_print("debug", responseresult, "HuoQuGeJiFenLeiBiaoQianChecklisten")
        logger.log_print("debug", sqlgetlist, "HuoQuGeJiFenLeiBiaoQianChecklisten")
    
        result = False
        j = 1
        for lss in sqlresult:
            for data in responseresult["data"]["lecture"]["child"]:
                if str(data["value"]) == str(j):
                    for ls in lss:
                        result = False
                        logger.log_print("debug", ls, "HuoQuGeJiFenLeiBiaoQianChecklisten")
                        for x in data["child"]:
                            if str(x.get("id")) == str(ls[0]):
                                logger.log_print("debug", x, "HuoQuGeJiFenLeiBiaoQianChecklisten")
                                i = 0
                                for s in sqlgetlist:
                                    logger.log_print("debug", "@" + s + "@ >> " + str(x.get(s)) + " ?? " + str(ls[i]), "HuoQuGeJiFenLeiBiaoQianChecklisten" )
                                    assert CheckSQLGet.Check(ls[i], x.get(s)) is True
                                    result = True    
                                    i += 1     
                                break
                    assert result==True
            j += 1
        

        result = False
        for data in responseresult["data"]["lecture"]["child"]:
            j = 1
            for lss in sqlresult:
                if str(data["value"]) == str(j):
                    for x in data["child"]:
                        result = False
                        logger.log_print("debug", ls, "HuoQuGeJiFenLeiBiaoQianChecklisten")
                        for ls in lss:
                            if str(x.get("id")) == str(ls[0]):
                                logger.log_print("debug", x, "HuoQuGeJiFenLeiBiaoQianChecklisten")
                                i = 0
                                for s in sqlgetlist:
                                    logger.log_print("debug", "@" + s + "@ >> " + str(x.get(s)) + " ?? " + str(ls[i]) , "HuoQuGeJiFenLeiBiaoQianChecklisten")
                                    assert CheckSQLGet.Check(ls[i], x.get(s)) is True
                                    i += 1     
                                result = True 
                                break
                            
                    assert result==True
                j += 1
        logger.log_print("debug", "<===========================================================")
        return result

        
    @staticmethod
    def HuoQuGeJiFenLeiBiaoQianCheckspeaking(sqlresult, responseresult, sqlgetlist, **kwargs):
        # TODO :check 
        logger.log_print("debug", "===========================================================>")
        logger.log_print("debug", sqlresult, "HuoQuGeJiFenLeiBiaoQianCheckspeaking")
        logger.log_print("debug", responseresult, "HuoQuGeJiFenLeiBiaoQianCheckspeaking")
        logger.log_print("debug", sqlgetlist, "HuoQuGeJiFenLeiBiaoQianCheckspeaking")
    
        result = False
        l = ["67","78","85","90","97","103"]
        j = 1
        x1 = 0
        for lss in sqlresult:
            for data in responseresult["data"].values():
                if str(data["id"]) == str(l[x1]):
                    for ls in lss:
                        result = False
                        logger.log_print("debug", ls, "HuoQuGeJiFenLeiBiaoQianCheckspeaking")
                        for x in data["child"]:
                            if str(x.get("id")) == str(ls[0]):
                                logger.log_print("debug", x, "HuoQuGeJiFenLeiBiaoQianCheckspeaking")
                                i = 0
                                for s in sqlgetlist:
                                    logger.log_print("debug","@" + s + "@ >> " + str(x.get(s)) + " ?? " + str(ls[i]), "HuoQuGeJiFenLeiBiaoQianCheckspeaking" )
                                    assert CheckSQLGet.Check(ls[i], x.get(s)) is True
                                    result = True    
                                    i += 1     
                                break
                    assert result==True
            j += 1
            x1 += 1
        
        logger.log_print("debug", "ok on first check------------------------------------------", "HuoQuGeJiFenLeiBiaoQianCheckspeaking")
        

        result = False
        for data in responseresult["data"].values():
            x1 = 0
            for lss in sqlresult:
                logger.log_print("debug", x1, "HuoQuGeJiFenLeiBiaoQianCheckspeaking")
                if str(data["id"]) == str(l[x1]):
                    for x in data["child"]:
                        for ls in lss:
                            if str(x.get("id")) == str(ls[0]):
                                logger.log_print("debug", x, "HuoQuGeJiFenLeiBiaoQianCheckspeaking")
                                i = 0
                                for s in sqlgetlist:
                                    logger.log_print("debug","@" + s + "@ >> " + str(x.get(s)) + " ?? " + str(ls[i]) , "HuoQuGeJiFenLeiBiaoQianCheckspeaking")
                                    assert CheckSQLGet.Check(ls[i], x.get(s)) is True
                                    i += 1
                                result = True
                                break
                    break
                x1 += 1
            assert result

        logger.log_print("debug", "<===========================================================")
        return result
    
    @staticmethod
    def HuoQuGeJiFenLeiBiaoQianCheckwriting(sqlresult, responseresult, sqlgetlist, **kwargs):
        sqlcheck.HuoQuGeJiFenLeiBiaoQianCheck(sqlresult, responseresult, sqlgetlist, "integrated_writing", **kwargs)

    @staticmethod
    def BiaoQianShaiXuanCheck(sqlresult, responseresult, sqlgetlist, other=None, funcname1=None, **kwargs):
        funcname = "BiaoQianShaiXuanCheck"
        if funcname is not None:
            funcname = funcname1
        logger.log_print("debug", "===========================================================>")
        logger.log_print("debug", sqlresult, funcname)
        logger.log_print("debug", responseresult, funcname)
        logger.log_print("debug", sqlgetlist, funcname)
        
        default_name = ["学科分类", "题型"]
        if other is not None:
            default_name = other

        index = 0
        for dn in default_name:
            result = False
            for ls in sqlresult[index]:
                logger.log_print("debug", ls, funcname)
                result = False
                for data in responseresult["data"][dn]:
                    if data.get("id") == str(ls[0]):
                        i = 0
                        for l in ls:
                            logger.log_print("debug","@" + sqlgetlist[i] + "@ >> " + str(data.get(sqlgetlist[i])) + " ?? " + str(l), funcname)
                            assert CheckSQLGet.Check(l, data.get(sqlgetlist[i])) is True
                            result = True
                            i += 1             
                assert result
            logger.log_print("debug", "ok on first check------------------------------------------", funcname)
            for data in responseresult["data"][dn]:
                logger.log_print("debug", data, funcname)
                result = False
                for ls in sqlresult[index]:     
                    if data.get("id") == str(ls[0]):
                        i = 0
                        for l in ls:
                            logger.log_print("debug", "@" + sqlgetlist[i] + "@ >> " + str(data.get(sqlgetlist[i])) + " ?? " + str(l), funcname)
                            assert CheckSQLGet.Check(l, data.get(sqlgetlist[i])) is True
                            result = True
                            i += 1             
                assert result
            index += 1
            
        logger.log_print("debug", "<===========================================================")
        return result

    @staticmethod
    def BiaoQianShaiXuanCheckBtype2(sqlresult, responseresult, sqlgetlist, **kwargs):
        return sqlcheck.BiaoQianShaiXuanCheck(sqlresult, responseresult, sqlgetlist, ["题型", "讲座", "对话"], "BiaoQianShaiXuanCheckBtype2", **kwargs)

    @staticmethod
    def BiaoQianShaiXuanCheckBtype3(sqlresult, responseresult, sqlgetlist, **kwargs):
        return sqlcheck.BiaoQianShaiXuanCheck(sqlresult, responseresult, sqlgetlist, ["独立口语Task1话题", "独立口语Task2话题", "综合口语Task3话题", "综合口语Task4话题", "综合口语Task5话题", "综合口语Task6话题"], "BiaoQianShaiXuanCheckBtype3", **kwargs)

    @staticmethod
    def BiaoQianShaiXuanCheckBtype4(sqlresult, responseresult, sqlgetlist, **kwargs):
        return sqlcheck.BiaoQianShaiXuanCheck(sqlresult, responseresult, sqlgetlist, ["独立写作话题", "综合写作学科"], "BiaoQianShaiXuanCheckBtype4", **kwargs)

    @staticmethod
    def HuoQuBiaoQianGaiYaoCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        i = 0
        for l in sqlgetlist:
            logger.log_print("debug", l + " >> " + str( responseresult["data"].get(l)) + " ?? " + str(sqlresult[0][0][i]), "HuoQuBiaoQianGaiYaoCheck")
            assert CheckSQLGet.Check(str(sqlresult[0][0][i]),  responseresult["data"].get(l) )
            i += 1

        return True

    @staticmethod
    def ShengChengWorkFlowCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        if "testcase" in kwargs:
            testcase = kwargs["testcase"]
        else:
            return False
        assert sqlcheck.sqlcheck2(sqlresult[0][0], responseresult, sqlgetlist)
        api_request_data = testcase.api_request_data
        assert sqlcheck.sqlcheck3(sqlresult[1][0], api_request_data, api_request_data.keys())
        return True
    
    @staticmethod
    def ChaXunWorkFlowXiangQingCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        if responseresult["data"] in [None, []] and len(sqlresult[0]) == 0:
            return True
        return sqlcheck.sqlcheck2(sqlresult[0][0], responseresult, sqlgetlist)

    @staticmethod
    def GengXinWorkFlowCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        if "testcase" in kwargs:
            testcase = kwargs["testcase"]
        else:
            return False
        if responseresult["data"] in [None, []] and len(sqlresult[0]) == 0:
            return True
        return sqlcheck.sqlcheck2(sqlresult[0][0] if len(sqlresult[0]) > 0 else sqlresult[0], testcase.api_request_data, sqlgetlist, id="status", **kwargs)

    @staticmethod
    def ShanChuWorkFlowCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        result = {"data":{"status":9}}
        return sqlcheck.sqlcheck2(sqlresult[0][0], result, sqlgetlist)

    @staticmethod
    def GetPaperPracticeCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        if responseresult["data"] in [None, []] and len(sqlresult[0]) == 0:
            return True
        return sqlcheck.sqlcheck2(sqlresult[0][0] if len(sqlresult[0]) > 0 else sqlresult[0], responseresult, sqlgetlist, **kwargs)
    
    @staticmethod
    def GetPracticeStatusCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        return sqlcheck.sqlcheck1(sqlresult[0], responseresult, sqlgetlist, id="paper_id", **kwargs)

    @staticmethod
    def AstArticlePracticeSummaryCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        return sqlcheck.sqlcheck1(sqlresult[0], responseresult, sqlgetlist, id="workflow_id", **kwargs)

    @staticmethod
    def UserVocabularyListCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        return sqlcheck.sqlcheck1(sqlresult[0], responseresult, sqlgetlist, id="word", dataother="rows", **kwargs)

    @staticmethod
    def ArticleVocabularyListCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        return sqlcheck.sqlcheck1(sqlresult[0], responseresult, sqlgetlist, id="origin_id", dataother="rows", **kwargs)

    @staticmethod
    def LabelVocabularyListCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        return sqlcheck.sqlcheck1(sqlresult[0], responseresult, sqlgetlist, id="word_id", dataother="rows", **kwargs)

    @staticmethod
    def GetAnswerByTopicIdCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        return sqlcheck.sqlcheck1(sqlresult[0], responseresult, sqlgetlist, id="id", dataothers="data", **kwargs)

    @staticmethod
    def GetBizPracticeCountCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        if responseresult["data"] in [None, []] and len(sqlresult[0]) == 0:
            return True
        return sqlcheck.sqlcheck2(sqlresult[0][0] if len(sqlresult[0]) > 0 else sqlresult[0], responseresult, sqlgetlist, **kwargs)

    @staticmethod
    def WordTransCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        assert sqlcheck.sqlcheck3(sqlresult[0][0], responseresult["data"]["data"][0], sqlgetlist[0], **kwargs)
        assert sqlcheck.sqlcheck1(sqlresult[1], responseresult["data"]["data"][0]["origin"]["prons"], sqlgetlist[1], dataofown=True, id="pron_us", **kwargs)
        assert sqlcheck.sqlcheck1(sqlresult[2], responseresult["data"]["data"][0]["origin"]["examples"], sqlgetlist[2], dataofown=True, id="example", **kwargs)
        return True
    
    @staticmethod
    def WordExamplesCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        assert sqlcheck.sqlcheck1(sqlresult[0], responseresult, sqlgetlist, id="example", **kwargs)
        return True

    @staticmethod
    def LabelHasWordCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        if sqlresult[0][0][0] > 0:
            assert responseresult["data"]["hasWord"] == True
        else:
            assert responseresult["data"]["hasWord"] == False
        return True

    @staticmethod
    def UserArticleNewWordCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        if len(sqlresult[0]) == 0 and len(responseresult["data"]) == 0:
            return True
        return sqlcheck.sqlcheck1(sqlresult[0], responseresult, sqlgetlist, id=[["word",0], ["count",2]], **kwargs)

    @staticmethod
    def ArticleKeyWordCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        if len(sqlresult[0]) == 0 and len(responseresult["data"]) == 0:
            return True
        return sqlcheck.sqlcheck1(sqlresult[0], responseresult, sqlgetlist, id=[["word_id",2]], **kwargs)
        
    @staticmethod
    def FeedBackCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        testcase = kwargs["testcase"]
        if len(testcase.sql_setup_result[0]) == 0:
            if sqlresult[0][0][0] == 1:
                return True
        else:
            if testcase.sql_setup_result[0][0][0] + 1 == sqlresult[0][0][0]:
                return True
        return False

    @staticmethod
    def RelationCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        # TODO 添加其他检查
        assert sqlcheck.sqlcheck1(sqlresult[0], responseresult["data"]["wordRelate"], sqlgetlist[0], dataofown=True, id=[["origin_id", 2]], **kwargs)
        assert sqlcheck.sqlcheck1(sqlresult[2], responseresult["data"]["transfrom"], sqlgetlist[2], dataofown=True, id=[["word", 0]], **kwargs)
        return True

    @staticmethod
    def IsNewWordCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        if sqlresult[0][0][0] == 0:
            return responseresult["data"] == False
        else:
            return responseresult["data"] == True

    @staticmethod
    def SearchRankCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        from haf.pylib.SQL.RedisTool import RedisTool
        import time, json
        from haf.check.CheckHttpResponse import CheckHttpResponse
        testcase = kwargs["testcase"]
        rankstr = "corpus:vocabulary:search:rank:" + time.strftime("%Y-%m-%d", time.localtime(time.time()))
        logger.log_print("info", rankstr)
        sr = json.loads(RedisTool.ConnectAndExecute(testcase.sql_config, rankstr, rev=True, start=0, end=0)[0])
        logger.log_print("info", sr)
        result = CheckHttpResponse.CheckJson(sr, responseresult["data"][0], [])
        logger.log_print("info", result)
        return result

    @staticmethod
    def RelateArticlesCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        assert sqlcheck.sqlcheck1(sqlresult[0], responseresult["data"], sqlgetlist, dataofown=True, id=[["article_id", 1]], **kwargs)
        return True
    
    @staticmethod
    def RelateWordsCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        assert sqlcheck.sqlcheck1(sqlresult[0], responseresult["data"]["relateWords"], sqlgetlist[0], dataofown=True, id=[["origin_id", 2]], **kwargs)
        return True

    @staticmethod
    def LabelListCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        assert sqlcheck.sqlcheck1(sqlresult[0], responseresult["data"], sqlgetlist[0],  dataofown=True, id=[["labelname", 1]], **kwargs)
        
        return True
    
    @staticmethod
    def WordLabelCheck(sqlresult, responseresult, sqlgetlist, **kwargs):
        assert sqlcheck.sqlcheck1(sqlresult[0], responseresult["data"], sqlgetlist[0],  dataofown=True, id=[["id", 2]], **kwargs)
        return True