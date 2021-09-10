from datetime import datetime

def convert_UTC_datetime_to_unix_time(datetime_obj):
    return (datetime_obj - datetime(1970, 1, 1)).total_seconds()