import os

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

from constants import INPUT_VIDEO, PROCESS_VIDEO, RESOURCES_FOLDER
from logger import logger


def save_process_video(duration=int, input_video: str = INPUT_VIDEO, output_video: str = PROCESS_VIDEO):
    original_video = VideoFileClip(RESOURCES_FOLDER + input_video)
    video_with_analysis = VideoFileClip(RESOURCES_FOLDER + output_video)

    tmp_audio_path = "tmp_audio_" + input_video
    tmp_audio_path_clipped = "tmp_audio_clipped_" + input_video
    process_video_with_audio = "processed_with_audio_" + output_video

    original_video.audio.write_audiofile(RESOURCES_FOLDER + tmp_audio_path, codec="mp3")

    audio_clip = AudioFileClip(RESOURCES_FOLDER + tmp_audio_path)
    logger.info(f"Audio duration: {audio_clip.duration}")

    audio_clipped = audio_clip.subclipped(start_time=0, end_time=duration)

    audio_clipped.write_audiofile(RESOURCES_FOLDER+tmp_audio_path_clipped, codec="mp3")

    video_with_analysis.write_videofile(
        RESOURCES_FOLDER + process_video_with_audio,
        codec="libx264",
        fps=video_with_analysis.fps,
        audio=RESOURCES_FOLDER+tmp_audio_path_clipped,
        audio_codec="aac"
    )

    os.remove(RESOURCES_FOLDER + tmp_audio_path)
    os.remove(RESOURCES_FOLDER + tmp_audio_path_clipped)
    os.remove(RESOURCES_FOLDER + output_video)
