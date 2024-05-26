from datetime import datetime


def convert_time_to_12_hour_format(time_obj):
    time_as_datetime = datetime.strptime(str(time_obj), "%H:%M:%S")
    return time_as_datetime.strftime("%I:%M %p")