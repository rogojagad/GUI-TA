from flask import Flask, render_template, request
from process_controller import ProcessController
from pprint import pprint
import json

app = Flask(__name__)
controller = object()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    sentence = request.get_json(silent=True)["sentence"]
    pprint(sentence)
    # sentence = request.get_json(force=True)["sentence"]

    return json.dumps(controller.start_process(sentence))
    # return request.form.get("sentence")


@app.before_first_request
def initialize():
    global controller
    controller = ProcessController()


if __name__ == "__main__":
    app.run(debug=True)
