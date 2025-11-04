#!/usr/bin/env python3
"""
downloader.py
Contains functions to download files, YouTube videos, and apps
"""

import os
import logging
import requests
import youtube_dl
from urllib.parse import urlparse

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Downloader:
    def __init__(self, config):
        self.download_folder = getattr(config, "download_folder", "./downloads")
        os.makedirs(self.download_folder, exist_ok=True)

    def download_file(self, url: str):
        try:
            logger.info(f"Downloading: {url}")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            filename = os.path.join(self.download_folder, os.path.basename(urlparse(url).path) or "file")
            with open(filename, "wb") as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)
            logger.info(f"Saved file: {filename}")
            return filename
        except Exception as e:
            logger.exception(f"Failed to download file: {e}")
            return None

    def download_youtube_video(self, url: str):
        ydl_opts = {
            'outtmpl': os.path.join(self.download_folder, '%(title)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'noplaylist': True
        }
        try:
            logger.info(f"Downloading YouTube video: {url}")
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            logger.exception(f"Failed to download YouTube video: {e}")
            return None

    def download_app(self, url: str):
        return self.download_file(url)

# Optional standalone test
if __name__ == "__main__":
    class DummyConfig:
        download_folder = "./downloads"

    d = Downloader(DummyConfig())
    test_url = input("Enter URL to download: ")
    d.download_file(test_url)
