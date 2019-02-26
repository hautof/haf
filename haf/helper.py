# encoding='utf-8'
import os, sys
from haf.config import *


class Helper(object):
    def __init__(self):
        pass
        # include init_workspace

    def init_workspace(self, case_type: str=None):
        ''' init haf workspace with type case'''
        if case_type:
            pass
        else:
            self.get_files_from_github()

    def get_files_from_github(self):
        os.system("git clone https://github.com/tsbxmw/haf-sample")
        