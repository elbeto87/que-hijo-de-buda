import os
import argparse

from face_recognition import emotions_detector
from logger import logger
from save_process_video import save_process_video

from youtube_downloader import download_video


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=None, help="Tiempo de duración del video")
    parser.add_argument("--youtube-link", type=str, help="Youtube link", default="https://www.youtube.com/watch?v=ij5_1zfmhOg")
    args = parser.parse_args()
    if not os.path.isfile("/home/elbeto87/Desktop/projects/que-hijo-de-buda/resources/video_to_analyze.mp4"):
        download_video(args.youtube_link)
    logger.info("Video has been already downloaded")
    emotions_detector(duration=args.duration)
    save_process_video(duration=args.duration)
