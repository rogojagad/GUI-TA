from flask import Flask, render_template, request, jsonify
from process_controller import ProcessController
from pprint import pprint

app = Flask(__name__)
controller = object()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    pprint(request.get_json(force=True))
    # sentence = request.get_json(silent=True, force=True)["sentence"]
    sentence = request.get_json(force=True)["sentence"]

    return jsonify(controller.start_process(sentence))
    # return request.form.get("sentence")


@app.before_first_request
def initialize():
    global controller
    controller = ProcessController()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
