from jinja2.loaders import FileSystemLoader
from latex.jinja2 import make_env
from latex import build_pdf

env = make_env(loader=FileSystemLoader("./templates/"))
template = env.get_template("opinion.tex")

pdf = build_pdf(template.render(text="test"))

with open("opinions/test.pdf", "wb") as f:
    f.write(bytes(pdf))
