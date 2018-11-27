# encoding='utf-8'
import os

from coupling.dict import AttrDict
from jinja2 import Environment, PackageLoader, FileSystemLoader


if __name__ == "__main__":
    path = os.path.dirname(__file__)
    print(path)
    j2r = FileSystemLoader("../resource/report/")
    j2r_e = Environment(loader=j2r, trim_blocks=True, lstrip_blocks=True, autoescape=True)
    j2r_t = j2r_e.get_template("base.html")
    result = {
        "begin_time":"",
        "end_time":"",
        "duration":"",
        "pass":0,
        "fail":0,
        "skip":0,
        "error":0,
        "details":[
            {
                "suite_name":"",
                "cases":[
                    {},
                    {}
                ]

            },
            {}
        ]
    }
    stream = j2r_t.stream(navigation=[1,2,3], a_variable="123123123")
    stream.dump()









