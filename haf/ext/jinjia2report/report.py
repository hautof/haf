# encoding='utf-8'
import os

from jinja2.environment import TemplateStream

from haf.result import EndResult
from jinja2 import Environment, FileSystemLoader
from haf.common.log import Log
from haf.utils import Utils
import traceback

logger = Log.getLogger(__name__)


class Jinja2Report(object):
    def __init__(self):
        pass

    @staticmethod
    def get_template_customer(path_: str) -> None:
        path, template = Utils.get_path(path_)
        j2r = FileSystemLoader(f"{path}")
        j2r_e = Environment(loader=j2r, trim_blocks=True, lstrip_blocks=True, autoescape=True)
        j2r_t = j2r_e.get_template(template)
        return j2r_t

    @staticmethod
    def get_template(key: str) -> None:
        if key == "base":
            template = "base.html"
        elif key == "online":
            template = "base_online.html"
        else:
            template = key
            if os.path.exists(template):
                try:
                    logger.info(f"try using customer template {template}")
                    return Jinja2Report.get_template_customer(template)
                except Exception as e:
                    logger.error(f"Jinja2Report Customer Template Error : {traceback.format_exc()}")
                    logger.info("continue using default template to generate report !!!")
            template = "base.html"

        local_dir = os.path.dirname(__file__)
        j2r = FileSystemLoader(f"{local_dir}/../resource/report/")
        j2r_e = Environment(loader=j2r, trim_blocks=True, lstrip_blocks=True, autoescape=True)
        j2r_t = j2r_e.get_template(template)
        return j2r_t

    @staticmethod
    def report(results: EndResult, name="base"):
        if results is None:
            return {"status": "error", "msg": "results is None"}
        if not name:
            name = "base"
        template = Jinja2Report.get_template(name)
        return template.generate(results=results)

    @staticmethod
    def write_report_to_file(info, report_path: str):
        try:
            logger.info(f"generate report to {report_path}")
            stream = TemplateStream(info)
            stream.dump(report_path)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def report_online(results: EndResult):
        if results is None:
            return {"status": "error", "msg": "results is None"}
        template = Jinja2Report.get_template("online")
        return template.render(results=results)






