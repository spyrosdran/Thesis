from flask import Flask, request, jsonify
from flask_cors import CORS
from evaluator import Evaluator


# Creating the app, editing the CORS policy and initializing the evaluator
app = Flask("YouTube Sentiment Analysis")
CORS(app)
evaluator = Evaluator()


@app.route("/evaluate", methods=["GET"])
def evaluate_text():
    text = request.args.get("text")

    if text is None:
        return jsonify({"error": "Please provide a 'text' parameter in the query."}, 400)

    response = evaluator.evaluate(text)
    return jsonify(response)

@app.route("/evaluate/video", methods=["GET"])
def evaluate_video():
    url = request.args.get("url")

    if url is None:
        return jsonify({"error": "Please provide a YouTube video URL."}, 400)

    response = evaluator.evaluate_comments(url)

    return jsonify(response)


# Starting the server
app.run()
