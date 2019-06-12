from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    jsonify,
    redirect,
    url_for,
    flash,
)
import os
from threading import Thread
from uuid import uuid1

from generateOpinion import generateOpinion

app = Flask(__name__)
app.secret_key = os.urandom(16)


@app.route("/")
def index():
    return render_template("index.html")


# Starts the generate thread and returns redirect with uuid
@app.route("/generate", methods=["POST"])
def generate():
    uuid = str(uuid1())
    thread = Thread(
        target=generateOpinion,
        args=(
            request.form["justice"],
            request.form["petitioner"].upper(),
            request.form["respondent"].upper(),
            request.form["date"],
            request.form["circuit"],
            uuid,
        ),
        daemon=True,
    )

    thread.start()

    flash(uuid)
    return redirect(url_for("loading"))


# Redirected to after submit, renders loading page with function that pings /api/getOpinion
@app.route("/loading", methods=["GET"])
def loading():
    return render_template("loading.html")


# Pinged every two seconds after submit
# Checks if file has been made, if so tell client
@app.route("/api/checkProgress", methods=["GET"])
def checkProgress():
    filename = request.args.get("uuid", "") + ".pdf"

    if os.path.isfile("opinions/" + filename):
        return jsonify({"ready": True})
    else:
        return jsonify({"ready": False})


# Gets and returns the opinion
@app.route("/opinion", methods=["GET"])
def opinion():
    filename = request.args.get("uuid", "") + ".pdf"

    if os.path.isfile("opinions/" + filename):
        # send and delete the file
        # https://stackoverflow.com/questions/40853201/remove-file-after-flask-serves-it?rq=1
        def loadAndDelete():
            with open("opinions/" + filename, mode="rb") as f:
                yield from f

            os.remove("opinions/" + filename)

        res = app.response_class(loadAndDelete(), mimetype="application/pdf")
        res.headers.set("Content-Disposision", "attachment", filename="opinion.pdf")
        return res
    else:
        return "you messed up"
