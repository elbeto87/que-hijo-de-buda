import glob
import os

import whisper

from yt_dlp import YoutubeDL
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

from constants import (
    RESOURCES_FOLDER,
    INPUT_VIDEO_PATH,
    TMP_AUDIO_PATH,
    TMP_AUDIO_CLIPPED_PATH,
    OUTPUT_VIDEO_PATH,
    OUTPUT_VIDEO_WITH_AUDIO_PATH
)
from logger import logger


class MultimediaHandler:

    def __init__(self, youtube_url: str, duration: int = None):
        self.youtube_url = youtube_url
        self.duration = duration

    @staticmethod
    def audio_transcription_to_text():
        logger.info("Processing audio transcription")
        model = whisper.load_model("base")
        return model.transcribe(TMP_AUDIO_CLIPPED_PATH)

    @staticmethod
    def save_process_video():
        video_with_analysis = VideoFileClip(OUTPUT_VIDEO_PATH)
        video_with_analysis.write_videofile(
            OUTPUT_VIDEO_WITH_AUDIO_PATH,
            codec="libx264",
            fps=video_with_analysis.fps,
            audio=TMP_AUDIO_CLIPPED_PATH,
            audio_codec="aac"
        )

    @staticmethod
    def remove_temporary_files():
        temp_files = glob.glob(os.path.join(RESOURCES_FOLDER, "tmp*"))
        for file in temp_files:
            os.remove(file)

    def download_video(self):
        logger.info("Downloading videos")
        options = {
            "outtmpl": INPUT_VIDEO_PATH
        }
        with YoutubeDL(options) as ydl:
            ydl.download(self.youtube_url)
        logger.info("Video has been downloaded")

    def check_if_video_already_downloaded(self):
        logger.info("Check if video already downloaded")
        if not os.path.isfile("./resources/video_to_analyze.mp4"):
            self.download_video()
        logger.info("Video has been already downloaded")

    def save_original_audio_and_transcription(self):
        original_video = VideoFileClip(INPUT_VIDEO_PATH)
        original_video.audio.write_audiofile(TMP_AUDIO_PATH, codec="mp3")
        audio_clip = AudioFileClip(TMP_AUDIO_PATH)
        logger.info(f"Audio duration: {audio_clip.duration}")
        audio_clipped = audio_clip.subclipped(start_time=0, end_time=self.duration)
        audio_clipped.write_audiofile(TMP_AUDIO_CLIPPED_PATH, codec="mp3")
