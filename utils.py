from datetime import timedelta

# Takes total seconds and returns to hh:mm:ss format
def toTimeFormat(totalSeconds: int):
    return timedelta(seconds=totalSeconds)

# Takes time in hh:mm:ss format and returns total seconds
def fromTimeFormat(timeString: str):
    hours, minutes, seconds = timeString.split(':')
    totalSeconds = int(seconds)
    totalSeconds += int(minutes) * 60
    totalSeconds += int(hours) * 60 * 60
    return totalSeconds