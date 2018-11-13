#encoding='utf-8'
import ast

from haf.framework_corpus_api import FrameworkOfZhan
import os, sys
import argparse
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
    temp = {"ids":para.ids, "runpytest":para.runpytest}

    foz.runfromXlsx(filelist, public2tomcat=True, onefile=True, pytest=True,
                    tomcatpath=r"D:\workspace\mine\python\autotestframework\base\binary\tomcat\webapps\zhan",
                    **temp)

def RunPys():
    filelist = []
    for f in os.listdir("testcases"):
        if f.endswith(".py") and not f.startswith("~$"):
            filelist.append('testcases/' + f)
    foz = FrameworkOfZhan()
    foz.runfromPy(filelist, public2tomcat=True, tomcatpath=r"D:\workspace\\mine\\python\\autotestframework\\base\\binary\\tomcat\\webapps\\zhan\\")


def main():
    program = argparse.ArgumentParser()
    program.add_argument("--runpytest", "-rpt", required=False, type=ast.literal_eval, help="true for run, false for not run")
    program.add_argument("--ids", "-id", action="append", required=False, default=[], help="ids for testcases")

    args = program.parse_args()

    print(args)
    AutoRun(args)

main()