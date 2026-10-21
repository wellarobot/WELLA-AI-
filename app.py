import os, requests
from flask import Flask, request
app = Flask(__name__)

VERIFY_TOKEN = "WELLA_AI_SECURE_2026"
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_ID = "1380186178514196"
URL = f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages"

def wella_reply(msg):
    m = msg.lower()
    if "habari" in m or "mambo" in m:
        return "Habari! Karibu WELLA AI 🤖 Niko live kwenye Render! Unahitaji nini leo?"
    if "bei" in m:
        return "Bei yetu 20k/mwezi. Unataka kujiunga?"
    return f"Umesema: {msg}\n\nMimi WELLA AI Bot - niko tayari kukuhudumia! 🚀"

def send_msg(to, text):
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    data = {"messaging_product":"whatsapp","to":to,"type":"text","text":{"body":text}}
    requests.post(URL, headers=headers, json=data)

@app.route("/")
def home():
    return "WELLA AI IS LIVE"

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Fail", 403

@app.route("/webhook", methods=["POST"])
def hook():
    try:
        data = request.get_json()
        msg = data['entry'][0]['changes'][0]['value']['messages'][0]
        frm = msg['from']
        body = msg['text']['body']
        send_msg(frm, wella_reply(body))
    except Exception as e:
        print(e)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
