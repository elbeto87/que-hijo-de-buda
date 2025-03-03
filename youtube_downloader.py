from logger import logger
from yt_dlp import YoutubeDL


def download_videos(urls: str):
    logger.info("Downloading videos")
    options = {
        "outtmpl": f"/home/elbeto87/Desktop/projects/que-hijo-de-buda/milei.mp4"
    }
    with YoutubeDL(options) as ydl:
        ydl.download(urls)
    logger.info("Video has been downloaded")