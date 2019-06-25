from flask import Flask, render_template, request
from process_controller import ProcessController
import json

app = Flask(__name__)
controller = ProcessController()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    sentence = request.get_json()["sentence"]

    return json.dumps(controller.start_process(sentence))
    # return controller.start_process()


if __name__ == "__main__":
    app.run(debug=True)
