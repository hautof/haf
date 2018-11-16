# -*- encoding:utf-8 -*-

import logging

class Log:

    @staticmethod
    def getLogger(logger_name):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s [%(name)s] %(message)s')
        logger = logging.getLogger(logger_name)
        return logger

