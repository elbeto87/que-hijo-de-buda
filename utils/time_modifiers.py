def format_time(seconds: int) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def to_seconds(time_str: str) -> int:
    parts = list(map(int, time_str.split(":")))
    if len(parts) == 2:  # mm:ss
        minutes, seconds = parts
        return minutes * 60 + seconds
    elif len(parts) == 3:  # hh:mm:ss
        hours, minutes, seconds = parts
        return hours * 3600 + minutes * 60 + seconds
    else:
        raise ValueError("Invalid Format, this application supports mm:ss or hh:mm:ss")

def get_new_topic(topics, index: int):
    new_topic = topics[index]
    return new_topic, to_seconds(new_topic["start_time"]), to_seconds(new_topic["end_time"])
