from flask import Flask, request, jsonify
import os
import requests
from datetime import datetime

app = Flask(__name__)

# Optional Telegram (Render env vars)
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")


def send_to_telegram(text: str):
    if not TG_BOT_TOKEN or not TG_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TG_CHAT_ID, "text": text}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception:
        pass


@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "api",
        "time": datetime.utcnow().isoformat()
    })


@app.route("/data", methods=["POST"])
def receive_json():
    if not request.is_json:
        return jsonify({"error": "JSON required"}), 400

    data = request.get_json()
    send_to_telegram(f"📩 New JSON:\n{data}")
    return jsonify({"status": "received"}), 200


@app.route("/upload", methods=["POST"])
def upload_raw():
    raw = request.data
    if not raw:
        return jsonify({"error": "empty body"}), 400

    send_to_telegram(f"📁 Raw payload received | size={len(raw)} bytes")
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
