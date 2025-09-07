from flask import Flask, request, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route("/")
def index():
    # Load the default page
    return render_template("index.html")

@app.route("/emotionDetector", methods=["GET"])
def detect_emotion():
    # Get input text from query parameters
    text_to_analyze = request.args.get("text", "")

    if not text_to_analyze:
        return "Error: No text provided. Please provide ?text=your_sentence", 400

    # Call the emotion detector
    result = emotion_detector(text_to_analyze)

    if "error" in result:
        return f"Error from emotion detector: {result['error']}", 500

    # Extract values
    anger = result.get("anger", 0)
    disgust = result.get("disgust", 0)
    fear = result.get("fear", 0)
    joy = result.get("joy", 0)
    sadness = result.get("sadness", 0)
    dominant_emotion = result.get("dominant_emotion", "unknown")

    # Create formatted response
    formatted_response = (
        f"For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, "
        f"'fear': {fear}, 'joy': {joy}, 'sadness': {sadness}, "
        f"The dominant emotion is {dominant_emotion}."
    )

    return formatted_response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
