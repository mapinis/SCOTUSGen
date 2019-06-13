from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    jsonify,
    redirect,
    url_for,
    g,
)
import os
import dataset
from threading import Thread
from uuid import uuid1
from sqlalchemy.pool import NullPool

from generateOpinion import generateOpinion

app = Flask(__name__)


def get_db_table():
    if "db" not in g:
        g.db = dataset.connect(engine_kwargs={"poolclass": NullPool})

    return g.db, g.db["runningUUIDs"]


@app.teardown_appcontext
def close_db(err=None):
    if err:
        print(err)

    db = g.pop("db", None)

    if db:
        db.executable.close()


@app.route("/")
def index():
    return render_template("index.html")


# Starts the generate thread and returns redirect with uuid
@app.route("/generate", methods=["POST"])
def generate():
    db, table = get_db_table()
    uuid = str(uuid1())

    table.insert({"uuid": uuid})
    db.commit()

    close_db()

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

    return redirect(url_for("loading", uuid=uuid))


# Redirected to after submit, renders loading page with function that pings /api/getOpinion
@app.route("/loading", methods=["GET"])
def loading():
    db, table = get_db_table()
    uuid = request.args.get("uuid", "")

    if not table.find_one(uuid=uuid):
        print(f"loading: {uuid} not found")
        print("Running UUIDs:")
        for row in table:
            print(row["uuid"])
        close_db()
        return redirect(url_for("index"))

    close_db()
    return render_template("loading.html", uuid=uuid)


# Pinged every two seconds after submit
# Checks if file has been made, if so tell client
@app.route("/api/checkProgress", methods=["GET"])
def check_progress():
    db, table = get_db_table()
    uuid = request.args.get("uuid", "")

    if not table.find_one(uuid=uuid):
        print(f"checkProgress: {uuid} not found")
        print("Running UUIDs:")
        for row in table:
            print(row["uuid"])
        close_db()
        return "Bad UUID", 400

    close_db()
    filename = uuid + ".pdf"

    if os.path.isfile("opinions/" + filename):
        return jsonify({"ready": True}), 200
    else:
        return jsonify({"ready": False}), 200


# Gets and returns the opinion
@app.route("/opinion", methods=["GET"])
def opinion():
    db, table = get_db_table()
    uuid = request.args.get("uuid", "")

    if not table.find_one(uuid=uuid):
        print(f"opinion: {uuid} not found")
        print("Running UUIDs:")
        for row in table:
            print(row["uuid"])
        close_db()
        return redirect(url_for("index"))

    filename = uuid + ".pdf"

    if os.path.isfile("opinions/" + filename):

        table.delete(uuid=uuid)
        db.commit()
        close_db()

        # send and delete the file
        # https://stackoverflow.com/questions/40853201/remove-file-after-flask-serves-it?rq=1
        def load_and_delete():
            with open("opinions/" + filename, mode="rb") as f:
                yield from f

            os.remove("opinions/" + filename)

        res = app.response_class(load_and_delete(), mimetype="application/pdf")
        res.headers.set("Content-Disposision", "attachment", filename="opinion.pdf")
        return res
    else:
        close_db()
        return redirect(url_for("loading", uuid=uuid))
