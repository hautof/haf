# -*- coding: utf-8 -*-

from .BaseReport import BaseTestReport, BaseHtmlTestReport
from .HttpReport import HttpHtmlTestReport


class TestReportFactory:
    @classmethod
    def new_report(cls, style=None, *args, **kwargs) -> BaseTestReport:
        if style == BaseHtmlTestReport.STYLE or style is None:
            return BaseHtmlTestReport(*args, **kwargs)
        elif style == HttpHtmlTestReport.STYLE:
            return HttpHtmlTestReport(*args, **kwargs)
        else:
            raise ValueError("Unsupported TestReport with style {}".format(style))
