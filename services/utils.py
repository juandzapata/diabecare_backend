from datetime import datetime


def convert_time_to_12_hour_format(time_obj):
    # Convierte el objeto time a datetime
    time_as_datetime = datetime.strptime(str(time_obj), "%H:%M:%S")
    # Formatea la hora en formato 12 horas con AM/PM
    return time_as_datetime.strftime("%I:%M %p")