from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector  # <-- your function

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# REQUIRED path
@app.route("/emotionDetector", methods=["GET"])
def emotionDetector():
    text = request.args.get("textToAnalyze", default="", type=str)

    # Call analyzer (it will return all-None dict when upstream status_code == 400)
    result = emotion_detector(text)

    # Error handling: if dominant_emotion is None, show the required message
    if result.get("dominant_emotion") is None:
        return "Invalid text! Please try again!"

    # Otherwise, format the success response exactly as specified
    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
