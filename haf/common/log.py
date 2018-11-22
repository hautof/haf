# -*- encoding:utf-8 -*-

import logging


class Log:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s <%(process)d> [%(name)s] %(message)s')

    @staticmethod
    def getLogger(logger_name):
        logger = logging.getLogger(logger_name)
        return logger

