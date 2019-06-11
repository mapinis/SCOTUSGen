from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    jsonify,
    redirect,
    url_for,
    make_response,
)
import os
from threading import Thread
from uuid import uuid1

from generateOpinion import generateOpinion

app = Flask(__name__)
app.secret_key = os.urandom(16)

runningUUIDs = []


@app.route("/")
def index():
    res = make_response(render_template("index.html"))
    res.set_cookie("uuid", "")
    return res


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
    runningUUIDs.append(uuid)

    res = make_response(redirect(url_for("loading")))
    res.set_cookie("uuid", uuid)
    return res


# Redirected to after submit, renders loading page with function that pings /api/getOpinion
@app.route("/loading", methods=["GET"])
def loading():
    if request.cookies.get("uuid") not in runningUUIDs:
        res = make_response(redirect(url_for("index")))
        res.set_cookie("uuid", "")
        return res

    return render_template("loading.html")


# Pinged every two seconds after submit
# Checks if file has been made, if so tell client
@app.route("/api/checkProgress", methods=["GET"])
def checkProgress():
    uuid = request.cookies.get("uuid")

    if uuid not in runningUUIDs:
        return "Bad UUID Cookie", 400

    filename = uuid + ".pdf"

    if os.path.isfile("opinions/" + filename):
        return jsonify({"ready": True})
    else:
        return jsonify({"ready": False})


# Gets and returns the opinion
@app.route("/opinion", methods=["GET"])
def opinion():
    uuid = request.cookies.get("uuid")

    if uuid not in runningUUIDs:
        res = make_response(redirect(url_for("index")))
        res.set_cookie("uuid", "")
        return res

    filename = uuid + ".pdf"

    if os.path.isfile("opinions/" + filename):
        # send and delete the file
        # https://stackoverflow.com/questions/40853201/remove-file-after-flask-serves-it?rq=1
        def loadAndDelete():
            with open("opinions/" + filename, mode="rb") as f:
                yield from f

            os.remove("opinions/" + filename)
            runningUUIDs.remove(uuid)

        res = app.response_class(loadAndDelete(), mimetype="application/pdf")
        res.headers.set("Content-Disposision", "attachment", filename="opinion.pdf")
        res.set_cookie("uuid", "")
        return res
    else:
        return "you messed up"
