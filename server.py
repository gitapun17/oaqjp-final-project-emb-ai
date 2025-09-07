from flask import Flask, render_template, request
import requests

# Primary + fallback endpoints
API_URLS = [
    "https://sn-watson-nlp.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict",
    "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict",
]
API_HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
API_TIMEOUT = 8

app = Flask(__name__)

def build_payload(text):
    return {"raw_document": {"text": text}}

def call_emotion_api(text):
    payload = build_payload(text)
    for url in API_URLS:
        try:
            resp = requests.post(url, json=payload, headers=API_HEADERS, timeout=API_TIMEOUT)
            if resp.status_code == 200:
                return resp
        except requests.RequestException:
            # try next URL
            continue
    return None

def extract_emotions(data):
    preds = data.get("emotion_predictions") or data.get("emotionPredictions")
    if isinstance(preds, list) and preds:
        emo = (preds[0] or {}).get("emotion") or {}
        keys = ["anger", "disgust", "fear", "joy", "sadness"]
        if all(k in emo for k in keys):
            return {k: float(emo[k]) for k in keys}
    return None

def dominant_emotion(emotions):
    best_k = None
    best_v = None
    for k, v in emotions.items():
        if best_v is None or v > best_v:
            best_k, best_v = k, v
    return best_k

def format_message(emotions, dom):
    return (
        "For the given statement, the system response is "
        f"'anger': {emotions['anger']}, "
        f"'disgust': {emotions['disgust']}, "
        f"'fear': {emotions['fear']}, "
        f"'joy': {emotions['joy']} and "
        f"'sadness': {emotions['sadness']}. "
        f"The dominant emotion is {dom}."
    )

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# REQUIRED path (exact)
@app.route("/emotionDetector", methods=["GET"])
def emotionDetector():
    text = request.args.get("textToAnalyze", default="", type=str)
    if not text or not text.strip():
        return "Invalid text! Try again.", 200

    resp = call_emotion_api(text)
    if resp is None:
        return "Invalid text! Try again.", 200

    data = resp.json()
    emotions = extract_emotions(data)
    if not emotions:
        return "Invalid text! Try again.", 200

    dom = dominant_emotion(emotions)
    if not dom:
        return "Invalid text! Try again.", 200

    return format_message(emotions, dom), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
