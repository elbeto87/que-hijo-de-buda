import os
import argparse

from face_recognition import emotions_detector
from logger import logger
from multimedia_handler import (
    save_process_video,
    save_original_audio_and_transcription,
    remove_temporary_files,
    audio_transcription_to_text,
)

from youtube_downloader import download_video


GLOBAL_CONTEXT = {
    "audio_transcription": None
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=None, help="Tiempo de duración del video")
    parser.add_argument("--youtube-link", type=str, help="Youtube link", default="https://www.youtube.com/watch?v=ij5_1zfmhOg")
    args = parser.parse_args()
    if not os.path.isfile("/home/elbeto87/Desktop/projects/que-hijo-de-buda/resources/video_to_analyze.mp4"):
        download_video(args.youtube_link)
    logger.info("Video has been already downloaded")
    save_original_audio_and_transcription(duration=args.duration)
    GLOBAL_CONTEXT["audio_transcription"] = audio_transcription_to_text()
    emotions_detector(duration=args.duration)
    save_process_video()
    remove_temporary_files()
