"""Flask app for EmotionDetection with clean, Pylint-friendly style."""
from flask import Flask, render_template, request

# Import the analyzer function from the EmotionDetection package
from EmotionDetection.emotion_detection import emotion_detector

ERROR_MESSAGE = "Invalid text! Please try again!"

app = Flask(__name__)


@app.route("/", methods=["GET"])  # pragma: no cover
def index() -> str:
    """Render the provided index.html from the templates folder."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET"])  # required route path
def emotion_detector_route() -> str:
    """Handle emotion detection requests and format the required response.

    Returns a human-readable sentence on success, or an error message when
    no dominant emotion is available (e.g., blank input).
    """
    text: str = request.args.get("textToAnalyze", default="", type=str)

    result = emotion_detector(text)

    # If the analyzer signals an invalid case, return the required message.
    if result.get("dominant_emotion") is None:
        return ERROR_MESSAGE

    anger = result["anger"]
    disgust = result["disgust"]
    fear = result["fear"]
    joy = result["joy"]
    sadness = result["sadness"]
    dominant = result["dominant_emotion"]

    return (
        "For the given statement, the system response is "
        f"'anger': {anger}, "
        f"'disgust': {disgust}, "
        f"'fear': {fear}, "
        f"'joy': {joy} and "
        f"'sadness': {sadness}. "
        f"The dominant emotion is {dominant}."
    )


if __name__ == "__main__":  # pragma: no cover
    app.run(host="0.0.0.0", port=5000)
