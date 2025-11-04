#!/usr/bin/env python3
"""
TRIZZY-AI-UNIT WhatsApp Cloud API Bot
Handles incoming WhatsApp messages and executes download commands
"""

import os
import json
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from Downloader import Downloader

# Load environment variables
load_dotenv()
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN")
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "./downloads")

# Ensure downloads folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Initialize downloader
downloader = Downloader(DOWNLOAD_FOLDER)

# Flask app
app = Flask(__name__)

# -----------------------------
# Webhook verification
# -----------------------------
@app.route('/webhook', methods=['GET'])
def verify():
    # Verify webhook token
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == "subscribe" and token == WEBHOOK_VERIFY_TOKEN:
        print("Webhook verified!")
        return str(challenge)
    else:
        return "Verification failed", 403

# -----------------------------
# Webhook to handle messages
# -----------------------------
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data.get("entry"):
        for entry in data["entry"]:
            for change in entry.get("changes", []):
                value = change.get("value")
                messages = value.get("messages", [])
                for message in messages:
                    phone = message["from"]
                    text = message.get("text", {}).get("body")
                    if text:
                        response = handle_message(text)
                        send_message(phone, response)
    return jsonify({"status": "received"}), 200

# -----------------------------
# Send WhatsApp message via API
# -----------------------------
def send_message(phone, message):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "text": {"body": message}
    }
    requests.post(url, headers=headers, json=payload)

# -----------------------------
# Command handler
# -----------------------------
def handle_message(message: str):
    message = message.strip()

    if message.startswith("/download_file "):
        url = message.split(" ", 1)[1]
        file_path = downloader.download_file(url)
        return f"✅ File saved: {file_path}" if file_path else "❌ Download failed."

    elif message.startswith("/download_video "):
        url = message.split(" ", 1)[1]
        success = downloader.download_youtube_video(url)
        return "✅ YouTube video downloaded!" if success else "❌ Download failed."

    elif message.startswith("/download_app "):
        url = message.split(" ", 1)[1]
        file_path = downloader.download_app(url)
        return f"✅ App saved: {file_path}" if file_path else "❌ Download failed."

    elif message == "/help":
        return (
            "TRIZZY-AI-UNIT Commands:\n"
            "/download_file
