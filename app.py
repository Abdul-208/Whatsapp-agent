from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import google.generativeai as genai
import os

app = Flask(__name__)

GEMINI_KEY = os.environ.get("GEMINI_KEY")
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_TOKEN = os.environ.get("TWILIO_TOKEN")
MY_NUMBER = os.environ.get("MY_NUMBER")
AGENT_ON = os.environ.get("AGENT_ON", "false")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
client = Client(TWILIO_SID, TWILIO_TOKEN)

IMPORTANT_KEYWORDS = ["urgent", "emergency", "zaruri", "hospital", 
                       "accident", "important", "jaldi", "help", "please"]

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    if AGENT_ON != "true":
        return Response("", mimetype="text/xml")
    
    incoming = request.form.get("Body", "")
    caller = request.form.get("From", "Unknown")
    
    prompt = f"""
    Tum Abdul ke personal WhatsApp assistant ho.
    Kisi ne yeh message bheja: "{incoming}"
    
    Unhe Urdu mein ek short, polite jawab do (2 sentences max).
    Phir likho [IMPORTANT: YES] agar message zaruri lage, warna [IMPORTANT: NO]
    """
    
    result = model.generate_content(prompt)
    full_response = result.text
    is_important = "IMPORTANT: YES" in full_response
    ai_reply = full_response.split("[IMPORTANT")[0].strip()
    
    if is_important:
        client.messages.create(
            from_="whatsapp:+14155238886",
            to=MY_NUMBER,
            body=f"🚨 Zaruri Message!\n📞 From: {caller}\n💬 Message: {incoming}\n🤖 AI: {ai_reply}"
        )
    
    resp = MessagingResponse()
    resp.message(ai_reply)
    return Response(str(resp), mimetype="text/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
