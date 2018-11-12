# -*- coding: utf-8 -*-

import os
import jinja2

from abc import ABCMeta, abstractmethod
from coupling import fs

from haf.testcase.HttpApiTestCase import HttpApiTestCase

import logging
logger = logging.getLogger(__name__)


CURRENT_DIR = os.path.dirname(__file__)


class BaseTestReport(metaclass=ABCMeta):
    @property
    @abstractmethod
    def STYLE(self):
        pass

    @property
    @abstractmethod
    def TEMPLATE(self):
        pass

    def __init__(self, result: HttpApiTestCase, output: str=None) -> None:
        self.result = result
        self.output = output

    @abstractmethod
    def generate(self, filename: str=None) -> None:
        pass

    def as_email_mime_base(self):
        pass


class BaseHtmlTestReport(BaseTestReport):
    STYLE = "base"
    TEMPLATE = os.path.join(CURRENT_DIR, "html", "base.html")

    def __init__(self, result: HttpApiTestCase, output: str=None, template: str=None, extras: dict=None,
                 chart_position="head", chart_display="none", detail_display="block"):
        super().__init__(result, output)
        self.template_dirs = [os.path.join(CURRENT_DIR, "html")]

        if not template:
            template = self.TEMPLATE
        head, tail = os.path.split(template)
        self.template_dirs.append(head)
        self.template = tail

        self.extras = extras or {}
        self.chart_position = chart_position
        self.chart_display = chart_display
        self.detail_display = detail_display

    def __create_simple(self, filename: str) -> None:
        j2_loader = jinja2.FileSystemLoader(self.template_dirs)
        j2_env = jinja2.Environment(loader=j2_loader, trim_blocks=True, lstrip_blocks=True, autoescape=True)
        j2_env.filters["path_basename"] = os.path.basename
        j2_env.filters["path_dirname"] = os.path.dirname
        j2_env.filters["path_relpath"] = os.path.relpath
        j2_template = j2_env.get_template(self.template)

        output_dir = os.path.dirname(filename)
        stream = j2_template.stream(
            _result_=self.result,
            _output_dir_=output_dir,
            _chart_position_=self.chart_position,
            _chart_display_=self.chart_display,
            _detail_display_=self.detail_display,
            **self.extras
        )

        fs.mkdirs(output_dir)
        stream.dump(filename)

    def generate(self, filename=None) -> None:
        filename = filename or self.output
        logger.debug("Generating html test report into %s", filename)
        self.__create_simple(filename)
