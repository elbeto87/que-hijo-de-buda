class Topic:

    def __init__(self, start_time: int, end_time: int, title: str):
        self.start_time = start_time
        self.end_time = end_time
        self.title = title

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def get_title(self):
        return self.title
