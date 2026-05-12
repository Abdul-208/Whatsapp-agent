from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

AGENT_ON = os.environ.get("AGENT_ON", "false")

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    if AGENT_ON != "true":
        return Response("", mimetype="text/xml")
    resp = MessagingResponse()
    resp.message("Abdul abhi available nahi hain. Apna message chhor dein, woh jald jawab denge.")
    return Response(str(resp), mimetype="text/xml")

@app.route("/")
def home():
    return "Agent is running!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
