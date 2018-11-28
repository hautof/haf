# encoding='utf-8'
import os

from coupling.dict import AttrDict
from jinja2 import Environment, PackageLoader, FileSystemLoader


class Jinjia2Report(object):
    def __init__(self):
        pass

    @staticmethod
    def report(results:dict, report_path:str):
        local_dir = os.path.dirname(__file__)
        j2r = FileSystemLoader(f"{local_dir}/../resource/report/")
        j2r_e = Environment(loader=j2r, trim_blocks=True, lstrip_blocks=True, autoescape=True)
        j2r_t = j2r_e.get_template("base.html")
        stream = j2r_t.stream(results = results)
        stream.dump(report_path)









