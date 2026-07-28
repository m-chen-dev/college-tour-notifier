from datetime import datetime

def format_message(university: str, date_and_time : str | None = None):
    if date_and_time:
        return f"Opening at {university} at {date_and_time}!! 🚨🚨"
    
    return f"Opening at {university}!! 🚨🚨"

def log(*args):
    now = datetime.now()
    time_stamp = now.strftime("%I:%M:%S")
    print(f"[{time_stamp}] -", end=" ")
    print(*args)

def format_message_for_university(university: str):
    return f"Failed to find available date for {university}"

def format_toast_title(university : str):
    return f"Opening at {university}"
