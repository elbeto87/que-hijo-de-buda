import argparse

from analysis.video_analysis import VideoAnalysis


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, default=None, help="Youtube time duration")
    parser.add_argument(
        "--youtube-link",
        type=str,
        default="https://www.youtube.com/watch?v=ij5_1zfmhOg",
        help="Youtube URL link"
    )
    args = parser.parse_args()
    VideoAnalysis(duration=args.duration, youtube_url=args.youtube_link).process_video()
