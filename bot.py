#!/usr/bin/env python3
"""
bot.py
WhatsApp Downloader Bot
Listens for WhatsApp messages and executes download commands
"""

import os
from dotenv import load_dotenv
from downloader import Downloader

# Load environment variables
load_dotenv()

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN")
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "./downloads")

# Ensure downloads folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Initialize downloader
class Config:
    download_folder = DOWNLOAD_FOLDER

downloader = Downloader(Config())

# Mock WhatsApp message handler (replace with real WhatsApp API integration)
def handle_message(message: str):
    """
    message: string from WhatsApp
    """
    if message.startswith("/download_file "):
        url = message.split(" ", 1)[1]
        file_path = downloader.download_file(url)
        return f"File saved: {file_path}" if file_path else "Download failed."

    elif message.startswith("/download_video "):
        url = message.split(" ", 1)[1]
        success = downloader.download_youtube_video(url)
        return "YouTube video downloaded!" if success else "Download failed."

    elif message.startswith("/download_app "):
        url = message.split(" ", 1)[1]
        file_path = downloader.download_app(url)
        return f"App saved: {file_path}" if file_path else "Download failed."

    elif message == "/help":
        return "Commands:\n/download_file <url>\n/download_video <url>\n/download_app <url>"

    else:
        return "Unknown command. Type /help for commands."

# ----------------------------
# Example testing loop
# ----------------------------
if __name__ == "__main__":
    print("WhatsApp Downloader Bot (Mock) running...")
    while True:
        msg = input("Enter message: ")
        response = handle_message(msg)
        print("Bot:", response)
