import os
from logger import logger

from youtube_downloader import download_videos


if __name__ == '__main__':
    if not os.path.isfile("/home/elbeto87/Desktop/projects/que-hijo-de-buda/milei.mp4"):
        download_videos("https://www.youtube.com/watch?v=ij5_1zfmhOg")
    logger.info("Video has been already downloaded")
