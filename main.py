import os

from face_recognition import emotions_detector
from logger import logger
from save_process_video import save_process_video

from youtube_downloader import download_videos


if __name__ == '__main__':
    if not os.path.isfile("/home/elbeto87/Desktop/projects/que-hijo-de-buda/resources/milei.mp4"):
        download_videos("https://www.youtube.com/watch?v=ij5_1zfmhOg")
    logger.info("Video has been already downloaded")
    duration=10
    emotions_detector(duration=duration)
    save_process_video(duration=duration)
