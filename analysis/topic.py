from collections import defaultdict


class Topic:

    def __init__(self, start_time: int, end_time: int, title: str):
        self.start_time = start_time
        self.end_time = end_time
        self.title = title
        self.emotions = defaultdict(int)

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def get_title(self):
        return self.title

    def add_new_frame_emotion(self, emotion):
        if emotion != "Unknown":
            self.emotions["total_count"] += 1
            self.emotions[emotion] += 1

    def get_emotions_percentage(self):
        return {emotion: int(emotions_count / self.emotions["total_count"] * 100) for emotion, emotions_count in self.emotions.items() if emotion not in ["total_count", "Unknown"]}