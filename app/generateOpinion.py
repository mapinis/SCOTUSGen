from textgenrnn import textgenrnn
from jinja2.loaders import FileSystemLoader
from latex.jinja2 import make_env
from latex import build_pdf
from random import randint
import os

env = make_env(loader=FileSystemLoader("./templates/"))
template = env.get_template("opinion.tex")

textgen = textgenrnn(
    weights_path="../model/model_weights.hdf5",
    vocab_path="../model/model_vocab.json",
    config_path="../model/model_config.json",
)

textgen.model._make_predict_function()  # https://github.com/matterport/Mask_RCNN/issues/588

# Takes justice, petitioner, respondent, date, and circuit, and returns name of PDF of opinion
# Generates it all -- text, LaTeX, and compiles it
# Generated files are in format <UUID>.pdf
def generateOpinion(justice, petitioner, respondent, date, circuit, uuid):

    # Generate the text
    text = textgen.generate(
        prefix="The", temperature=0.72, max_gen_length=7000, return_as_list=True
    )[0]
    # Go to first instance of period, so start with sentence
    text = text[text.find(".") + 1 :]
    text = " ".join(text.split())  # Collapse spaces
    text = bytes(text, "utf-8").decode("utf-8", "ignore")  # Remove special characters

    # Insert newlines
    text = text.split(".")
    i = randint(4, 7)
    while i < len(text):
        text[i] = "\\\ \\newline " + text[i]
        i += randint(4, 7)

    # Put it all together and fix LaTeX tokens
    text = ".".join(text).replace("&", "\&").replace("%", "\%").replace("$", "\$")

    pdf = build_pdf(
        template.render(
            justice=justice,
            petitioner=petitioner,
            respondent=respondent,
            date=date,
            circuit=circuit,
            number1=str(randint(10, 99)),
            number2=str(randint(100, 999)),
            text=text + "." if text[-1] != "." else "",
        )
    )

    filename = uuid + ".pdf"

    if not os.path.isdir("opinions"):
        os.mkdir("opinions")

    with open("opinions/" + filename, "wb") as f:
        f.write(bytes(pdf))
