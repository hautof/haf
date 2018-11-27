# encoding='utf-8'
import os

from jinja2 import Environment, PackageLoader, FileSystemLoader


if __name__ == "__main__":
    path = os.path.dirname(__file__)
    print(path)
    j2r = FileSystemLoader("./")
    j2r_e = Environment(loader=j2r, trim_blocks=True, lstrip_blocks=True, autoescape=True)
    j2r_t = j2r_e.get_template("base.html")

    stream = j2r_t.stream(navigation=[1,2,3], a_variable="123123123")
    stream.dump()









