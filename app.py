from flask import Flask, request, jsonify
import requests
import os
import logging

app = Flask(__name__)

# === CONFIG YAKO ===
VERIFY_TOKEN = "WELLA_AI_SECURE_2026"
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN", "YOUR_LONG_TOKEN_HAPA")
PHONE_ID = "1380186178514196"  # ID ya 0749520061
PHONE_NUMBER = "0749520061"

logging.basicConfig(level=logging.INFO)

# === 1. VERIFY WEBHOOK (Facebook inaita) ===
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        logging.info("WEBHOOK VERIFIED!")
        return challenge, 200
    else:
        return "Verification failed", 403

# === 2. POKEA UJUMBE NA JIBU ===
@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    logging.info(f"Data received: {data}")
    
    try:
        if data.get("object") == "whatsapp_business_account":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    
                    for message in messages:
                        from_number = message.get("from")
                        text = message.get("text", {}).get("body", "")
                        
                        logging.info(f"Ujumbe kutoka {from_number}: {text}")
                        
                        # JIBU OTOMATIKI
                        reply_text = f"""Habari! Karibu WELLA AI 🤖

Umetuma: "{text}"

Niko live kwenye 0749520061!
Niko tayari kukusaidia:

1️⃣ Habari za leo
2️⃣ Huduma zetu
3️⃣ Ongea na binadamu

Andika neno unalotaka!"""

                        send_whatsapp_message(from_number, reply_text)
                        
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"status": "error"}), 200

def send_whatsapp_message(to_number, text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": text}
    }
    
    response = requests.post(url, headers=headers, json=payload)
    logging.info(f"Sent to {to_number}: {response.status_code} - {response.text}")
    return response

@app.route("/", methods=["GET"])
def home():
    return "WELLA AI Bot iko LIVE kwenye 0749520061! 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
