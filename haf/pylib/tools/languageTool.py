#encoding='utf-8'

import os, time, sys

from xpinyin import Pinyin
from haf.pylib.Log.LogController import LogController

class_name = "languageTool"
logger = LogController.getLogger(class_name)

class languageTool(object):
    def __init__(self):
        pass

    @staticmethod
    def ChineseJudge(source):
        for s in str(source):
            logger.log_print("debug", s)
            if '\u4e00' <= s <= '\u9fff':
                return True
        else :
            return False

    @staticmethod
    def Chinese2English(chinese):
        if languageTool.ChineseJudge(chinese):
            pinyin = Pinyin()
            return pinyin.get_pinyin(chinese).replace("-", "")

        return chinese