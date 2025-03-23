from constants import INPUT_VIDEO_PATH
from logger import logger
from yt_dlp import YoutubeDL


def download_video(urls: str):
    logger.info("Downloading videos")
    options = {
        "outtmpl": INPUT_VIDEO_PATH
    }
    with YoutubeDL(options) as ydl:
        ydl.download(urls)
    logger.info("Video has been downloaded")