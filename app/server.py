from flask import Flask, render_template, request, send_from_directory
import os

from generateOpinion import generateOpinion

app = Flask("SCOTUSGen")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/opinion", methods=["POST"])
def opinion():
    filename = generateOpinion(
        request.form["justice"],
        request.form["petitioner"],
        request.form["respondent"],
        request.form["arguedDate"],
        request.form["decisionDate"],
    )

    # send and delete the file
    # https://stackoverflow.com/questions/40853201/remove-file-after-flask-serves-it?rq=1
    def loadAndDelete():
        with open("opinions/" + filename, mode="rb") as f:
            yield from f

        os.remove("opinions/" + filename)

    res = app.response_class(loadAndDelete(), mimetype="application/pdf")
    res.headers.set("Content-Disposision", "attachment", filename="opinion.pdf")
    return res
