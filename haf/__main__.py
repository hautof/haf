#encoding='utf-8'
from haf.framework_corpus_api import FrameworkOfZhan
import os, sys
"""
this is main.py
执行整个框架的入口函数
"""
def LocalRun():
    '''
    本地 debug
    '''
    filelist = ["testcases/Template1.xlsx"]
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            filelist.append(arg)
    foz = FrameworkOfZhan()
    foz.runfromXlsx(filelist, public2tomcat=True, tomcatpath="/root/edison/tools/apache-tomcat-9.0.10/webapps/")

def AutoRun(para):
    '''
    自动读取所有的 testcases 文件
    '''
    filelist = []
    for f in os.listdir("testcases"):
        if f.endswith(".xlsx") and not f.startswith("~$"):
            filelist.append('testcases/' + f)
    foz = FrameworkOfZhan()
    if para is None:
        foz.runfromXlsx(filelist, public2tomcat=True, onefile=True, tomcatpath=r"D:\workspace\mine\python\autotestframework\base\binary\tomcat\webapps\zhan")
    else:
        foz.runfromXlsx(filelist, public2tomcat=True, onefile=True, tomcatpath=r"D:\workspace\mine\python\autotestframework\base\binary\tomcat\webapps\zhan", ids=para)


def RunPys():
    
    filelist = []
    for f in os.listdir("testcases"):
        if f.endswith(".py") and not f.startswith("~$"):
            filelist.append('testcases/' + f)
    foz = FrameworkOfZhan()
    foz.runfromPy(filelist, public2tomcat=True, tomcatpath=r"D:\workspace\\mine\\python\\autotestframework\\base\\binary\\tomcat\\webapps\\zhan\\")

def main():
    #LocalRun()
    print(sys.argv)
    if len(sys.argv) > 1:
        para = sys.argv[1:]
    else:
        para = None
    print(para)
    AutoRun(para)
    #RunPys()


main()