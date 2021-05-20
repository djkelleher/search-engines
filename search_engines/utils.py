from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import re


def extract_first(query_result):
    return str(query_result[0]).strip() if len(query_result) else ""


def extract_all(query_result):
    return [str(res).strip() for res in query_result]


def join_all(query_result, join_str=" "):
    return join_str.join([str(t).strip() for t in query_result]) if len(query_result) else ""


def publish_time(time_text: str):
    """Convert published time text like "2 hours ago" to a timestamp"""

    match = re.search(r'(?i)(\d+)\s*(year|month|week|day|hour|minute|second|min|sec)s?', time_text)
    if match:
        value, unit = re.search(r'(\d+) (\w+) ago', time_text).groups()
        if not unit.endswith('s'): unit += 's'
        delta = relativedelta(**{unit: int(value)})
        return (datetime.now() - delta).strftime('%Y-%m-%d %H:%M:%S')
    else:
        return parse(time_text, fuzzy=True).strftime('%Y-%m-%d %H:%M:%S')
