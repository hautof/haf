# -*- coding: utf-8 -*-

import os
from haf.pylib.Report.BaseReport import BaseHtmlTestReport


CURRENT_DIR = os.path.dirname(__file__)


class HttpHtmlTestReport(BaseHtmlTestReport):
    STYLE = "http"
    TEMPLATE = os.path.join(CURRENT_DIR, "html", "{}.html".format(STYLE))
