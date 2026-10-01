from flask import Flask, render_template, request, jsonify
from pathlib import Path
import re
import pickle

app = Flask(__name__)

MODEL_PATH = Path("models/message_model.pkl")

model = None
if MODEL_PATH.exists():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

URGENT_WORDS = [
    "urgent", "immediately", "act now", "within 24 hours", "account blocked",
    "account suspended", "verify now", "last warning", "limited time"
]
SENSITIVE_WORDS = [
    "otp", "pin", "password", "cvv", "bank details", "card number",
    "upi pin", "verification code"
]
MONEY_WORDS = [
    "transfer", "send money", "payment", "refund", "prize", "lottery",
    "cashback", "fee", "deposit"
]

def analyze_message(text):
    text_l = text.lower()
    indicators = []
    score = 0

    if any(w in text_l for w in URGENT_WORDS):
        indicators.append("Uses urgency or pressure to make you act quickly.")
        score += 25

    if any(w in text_l for w in SENSITIVE_WORDS):
        indicators.append("Requests sensitive information such as an OTP, PIN, password or card details.")
        score += 35

    if any(w in text_l for w in MONEY_WORDS):
        indicators.append("Mentions money, payment, refund, prize or a financial transaction.")
        score += 20

    if "http://" in text_l or "https://" in text_l or "www." in text_l:
        indicators.append("Contains a web link. Verify the destination independently before opening it.")
        score += 15

    ml_probability = None
    if model:
        try:
            ml_probability = float(model.predict_proba([text])[0][1])
            score += round(ml_probability * 40)
        except Exception:
            pass

    score = min(score, 100)

    if score >= 65:
        level = "High Risk"
        color = "high"
        action = "Do not click links or share OTPs, PINs, passwords or banking information. Verify through the organization's official website or phone number."
    elif score >= 30:
        level = "Caution"
        color = "caution"
        action = "Pause before responding. Check the sender and verify the information through an official channel."
    else:
        level = "Lower Risk"
        color = "low"
        action = "No strong warning indicators were detected, but stay cautious and verify important requests independently."

    if not indicators:
        indicators.append("No major warning indicator was detected by the current prototype.")

    return {
        "level": level,
        "color": color,
        "score": score,
        "indicators": indicators,
        "action": action
    }

def analyze_url(url):
    u = url.strip()
    ul = u.lower()
    indicators = []
    score = 0

    if not re.match(r"^https?://", ul):
        indicators.append("The address does not clearly use HTTP/HTTPS.")
        score += 10

    if "@" in u:
        indicators.append("Contains '@', which can be used to disguise the actual destination.")
        score += 35

    if re.search(r"https?://\d{1,3}(?:\.\d{1,3}){3}", ul):
        indicators.append("Uses an IP address instead of a normal domain name.")
        score += 30

    suspicious_terms = ["login", "verify", "update", "secure", "account", "wallet", "claim", "prize", "refund"]
    hits = [x for x in suspicious_terms if x in ul]
    if hits:
        indicators.append("Contains terms commonly seen in account, payment or prize-related links.")
        score += min(25, len(hits) * 8)

    if len(u) > 100:
        indicators.append("The URL is unusually long and should be checked carefully.")
        score += 10

    if ul.startswith("http://"):
        indicators.append("Uses HTTP rather than HTTPS.")
        score += 15

    score = min(score, 100)

    if score >= 65:
        level, color = "High Risk", "high"
        action = "Do not open the link. Visit the organization's official website by typing its address yourself."
    elif score >= 30:
        level, color = "Caution", "caution"
        action = "Do not enter personal or banking information until the destination is independently verified."
    else:
        level, color = "Lower Risk", "low"
        action = "No major URL warning pattern was detected, but this does not guarantee that the website is genuine."

    if not indicators:
        indicators.append("No major suspicious URL pattern was detected by the current prototype.")

    return {"level": level, "color": color, "score": score, "indicators": indicators, "action": action}

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/api/check-message")
def check_message():
    data = request.get_json(silent=True) or {}
    text = (data.get("message") or "").strip()
    if not text:
        return jsonify({"error": "Please enter a message."}), 400
    return jsonify(analyze_message(text))

@app.post("/api/check-url")
def check_url():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    if not url:
        return jsonify({"error": "Please enter a URL."}), 400
    return jsonify(analyze_url(url))

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
