from datetime import datetime, timedelta
import re


def extract_first(query_result):
    return str(query_result[0]).strip() if len(query_result) else ""


def extract_all(query_result):
    return [str(res).strip() for res in query_result]


def join_all(query_result, join_str=" "):
    return join_str.join([str(t).strip() for t in query_result]) if len(query_result) else ""


def publish_date_from_time(time_published_text):
    match = re.search(
        r'(?i)(\d{1,4})\s{1,4}(weeks?|days?|hours?|minutes?|seconds?)',
        time_published_text)
    if match:
        time, units = int(match.group(1)), match.group(2).lower()
        if 'week' in units:
            td = timedelta(weeks=time)
        elif 'day' in units:
            td = timedelta(days=time)
        elif 'hour' in units:
            td = timedelta(hours=time)
        elif 'minute' in units:
            td = timedelta(minutes=time)
        elif 'second' in units:
            td = timedelta(seconds=time)
        else:
            print(f"Unrecognized time units: {units}")
            return
        return (datetime.now() - td).strftime('%Y-%m-%d %H:%M:%S')
