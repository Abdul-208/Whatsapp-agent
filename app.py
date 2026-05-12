from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

AGENT_ON = os.environ.get("AGENT_ON", "false")

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    if AGENT_ON != "true":
        return Response("", mimetype="text/xml")
    incoming = request.form.get("Body", "")
    resp = MessagingResponse()
    resp.message("Abdul abhi available nahi hain. Apna message chhor dein, woh jald jawab denge. Shukriya!")
    return Response(str(resp), mimetype="text/xml")

@app.route("/")
def home():
    return "Agent is running!", 200
