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

IMPORTANT_KEYWORDS = ["urgent", "emergency", "zaruri", "hospital",
                       "accident", "important", "jaldi", "help"]

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    if AGENT_ON != "true":
        return Response("", mimetype="text/xml")

    incoming = request.form.get("Body", "")
    caller = request.form.get("From", "Unknown")

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
        json={
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": "system", "content": "Tum Abdul ke WhatsApp assistant ho. Urdu mein short jawab do. Agar message zaruri lage to jawab ke end mein [IMPORTANT: YES] likho, warna [IMPORTANT: NO]"},
                {"role": "user", "content": incoming}
            ]
        }
    )

    result = response.json()
    full_response = result["choices"][0]["message"]["content"]
    is_important = "IMPORTANT: YES" in full_response
    ai_reply = full_response.replace("[IMPORTANT: YES]", "").replace("[IMPORTANT: NO]", "").strip()

    if is_important:
        client.messages.create(
            from_="whatsapp:+14155238886",
            to=MY_NUMBER,
            body=f"🚨 Zaruri Message!\n📞 From: {caller}\n💬 Message: {incoming}\n🤖 AI: {ai_reply}"
        )

    resp = MessagingResponse()
    resp.message(ai_reply)
    return Response(str(resp), mimetype="text/xml")

@app.route("/")
def home():
    return "Agent is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
