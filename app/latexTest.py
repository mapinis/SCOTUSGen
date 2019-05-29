from jinja2.loaders import FileSystemLoader
from latex.jinja2 import make_env
from latex import build_pdf

env = make_env(loader=FileSystemLoader("./templates/"))
template = env.get_template("opinion.tex")

pdf = build_pdf(
    template.render(
        petitioner="APPLE INC.",
        respondent="ROBERT PEPPER",
        date="May 29, 2019",
        justice="Ginsburg",
        number1="27",
        number2="4664",
        circuit="NINTH",
        text="test",
    )
)

with open("opinions/test.pdf", "wb") as f:
    f.write(bytes(pdf))
