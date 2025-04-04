from analysis.face_recognition import emotions_detector
from utils.multimedia_handler import MultimediaHandler


class VideoAnalysis:

    def __init__(self, youtube_url: str, duration: int = None):
        self.multimedia_handler = MultimediaHandler(youtube_url=youtube_url, duration=duration)
        self.duration = duration
        self.audio_transcription = None
        self.topics = None

    def process_video(self):
        self.multimedia_handler.check_if_video_already_downloaded()
        self.multimedia_handler.save_original_audio_and_transcription()
        self.audio_transcription = self.multimedia_handler.audio_transcription_to_text()
        self.topics = self.multimedia_handler.get_topics(self.audio_transcription)
        emotions_detector(duration=self.duration, topics=self.topics)
        self.multimedia_handler.save_process_video()
        self.multimedia_handler.remove_temporary_files()
