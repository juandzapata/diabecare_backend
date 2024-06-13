from datetime import datetime


from datetime import datetime

def convert_time_to_12_hour_format(time_obj):
    """
    Converts a time object to a 12-hour format string.

    Args:
        time_obj (datetime.time): The time object to be converted.

    Returns:
        str: The time in 12-hour format (e.g., "03:30 PM").
    """
    time_as_datetime = datetime.strptime(str(time_obj), "%H:%M:%S")
    return time_as_datetime.strftime("%I:%M %p")