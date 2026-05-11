from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
import requests

app = Flask(__name__)

OPENROUTER_KEY = os.environ.get("GEMINI_KEY")
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_TOKEN = os.environ.get("TWILIO_TOKEN")
MY_NUMBER = os.environ.get("MY_NUMBER")
AGENT_ON = os.environ.get("AGENT_ON", "false")

client = Client(TWILIO_SID, TWILIO_TOKEN)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    if AGENT_ON != "true":
        return Response("", mimetype="text/xml")
    incoming = request.form.get("Body", "")
    caller = request.form.get("From", "Unknown")
    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "google/gemma-3-4b-it:free",
                "messages": [
                    {"role": "system", "content": "Tum Abdul ke WhatsApp assistant ho. Urdu mein short jawab do 2 sentences mein."},
                    {"role": "user", "content": incoming}
                ]
            },
            timeout=10
        )
        result = r.json()
        ai_reply = result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        ai_reply = "Abdul abhi available nahi hain, baad mein try karein."
    resp = MessagingResponse()
    resp.message(ai_reply)
    return Response(str(resp), mimetype="text/xml")

@app.route("/")
def home():
    return "Agent is running!", 200
