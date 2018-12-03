# encoding='utf-8'
import os

from jinja2.environment import TemplateStream

from haf.result import EndResult
from jinja2 import Environment, FileSystemLoader
from haf.common.log import Log

logger = Log.getLogger(__name__)


class Jinja2Report(object):
    def __init__(self):
        pass

    @staticmethod
    def get_template(key: str):
        if key == "base":
            template = "base.html"
        elif key == "online":
            template = "base_online.html"

        local_dir = os.path.dirname(__file__)
        j2r = FileSystemLoader(f"{local_dir}/../resource/report/")
        j2r_e = Environment(loader=j2r, trim_blocks=True, lstrip_blocks=True, autoescape=True)
        j2r_t = j2r_e.get_template(template)
        return j2r_t

    @staticmethod
    def report(results: EndResult):
        if results is None:
            return {"status": "error", "msg": "results is None"}
        template = Jinja2Report.get_template("base")
        return template.generate(results=results)

    @staticmethod
    def write_report_to_file(info, report_path: str):
        try:
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






