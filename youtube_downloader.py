from constants import VIDEO_TO_ANALYZE
from logger import logger
from yt_dlp import YoutubeDL


def download_video(urls: str):
    logger.info("Downloading videos")
    options = {
        "outtmpl": VIDEO_TO_ANALYZE
    }
    with YoutubeDL(options) as ydl:
        ydl.download(urls)
    logger.info("Video has been downloaded")