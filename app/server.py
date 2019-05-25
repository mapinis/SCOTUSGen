from flask import Flask, render_template

from generateOpinion import generateOpinion

app = Flask("SCOTUSGen")


@app.route("/")
def index():
    return render_template("index.html")

