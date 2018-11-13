'''
# LogShow.py
# functions :

# date : 20180730
# version : 1.0
# author : wei.meng
# desc : using to show logstr as same formate.
'''

import time
import os,sys
import logging

class LogShow(object):
    '''
    Framework logger 默认类，使用 logging 
    '''
    def __init__(self, logflag:str):
        self.class_name = 'LogShow'
        self.logflag = logflag
        self.log_set_rank()
        #[%(funcName)s] 
        logging.basicConfig(level = logging.INFO,format = '%(asctime)s %(levelname)s [%(name)s] %(message)s')
        self.logger = logging.getLogger(logflag)
         
    def __str__(self):
        return self.class_name

    def log_set_rank(self):
        self.log_rank = {
            "system" : "SYSTEM",
            "debug" : "DEBUG",
            "info" : "INFO", 
            "warn" : "WARN",
            "error" : "ERROR",
            "fatal" : "FATAL"
        }
        self.log_color = {
            "system" : "white",
            "debug" : "yellow",
            "info" : "blue", 
            "warn" : "red",
            "error" : "red",
            "fatal" : "red"
        }
        self.log_level_num = {
            "system" : 5 ,
            "debug"  : 4 ,
            "info"   : 3 ,
            "warn"   : 2 ,
            "error"  : 1 ,
            "fatal"  : 0 ,
        }

    def log_getsystime(self):
        '''
        获取 格式化后的 系统时间， 暂未使用
        '''
        #return time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()) )
        
        ct = time.time()
        local_time = time.localtime(ct)
        time_ = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        secs = (ct - int(ct)) * 1000
        timenow = "%s.%03d" % (time_, secs)
        return timenow


    # print log with 'rank' 'funcname' 'self.log_flag'
    def log_print(self, rank, log_str, funcname=None):
        '''
        log 输出方法

        :参数:

        * rank : str log 等级
        * log_str : str 输出的 log 信息
        * funcname : str 默认为 None , 调用的函数名称
        
        :return: None

        '''
        if funcname is None:
            temp = [self.log_getsystime(), self.logflag, self.log_rank[rank], str(log_str)]
            self.log_string = "{} [ {} ] ( {} ) {}".format(*temp)
            self.log_str_temp = log_str
            #print self.log_string
        else:
            temp = [self.log_getsystime(), self.logflag, self.log_rank[rank], str(funcname), str(log_str)]
            self.log_string = "{} [ {} ] ({}) [ {} ] {}".format(*temp)
            self.log_str_temp = '[{}] {}'.format(str(funcname),str(log_str))
            #print self.log_string
        try:
            if rank == 'system':
                self.logger.info(self.log_str_temp)
            if rank == 'info':
                self.logger.info(self.log_str_temp)
            if rank == 'debug':
                self.logger.debug(self.log_str_temp)
            if rank == 'error':
                self.logger.error(self.log_str_temp)
            if rank == 'fatal':
                self.logger.fatal(self.log_str_temp)
            if rank == 'warn':
                self.logger.warn(self.log_str_temp)
        except Exception as e:
            print(str(e))

        #self.log_save_to_file("./data/log", self.logflag + '.log')
        self.log_save_to_one_file('./data/log')

    # save log local/name
    def log_save_to_file(self, local:str, name:str):
        '''
        分类保存 log 到文件中
        '''
        try:            
            if not os.path.exists(local):
                os.makedirs(local)
            if not os.path.exists(local + '/' + name):
                f = open(local + '/' + name, 'w')
                f.close()
            flog = open(local + '/' + name, 'a')
            flog.write(self.log_string + '\n')
            flog.close()
        except Exception as e:
            print(str(e))
    
    # save to local/log.log
    def log_save_to_one_file(self, local:str):
        '''
        保存 log 到一个文件中
        '''
        try:            
            if not os.path.exists(local):
                os.makedirs(local)
            if not os.path.exists(local + '/log.log'):
                f = open(local + '/log.log', 'w')
                f.close()
            flog = open(local + '/log.log', 'a')
            flog.write(self.log_string + '\n')
            flog.close()
        except Exception as e:
            print(str(e))

    