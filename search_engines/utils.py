from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse, ParserError
import re


def extract_first(query_result):
    return str(query_result[0]).strip() if len(query_result) else ""


def extract_all(query_result):
    return [str(res).strip() for res in query_result]


def join_all(query_result, join_str=" "):
    return join_str.join([str(t).strip() for t in query_result]) if len(query_result) else ""


def publish_time(time_text: str):
    """Convert published time text like "2 hours ago" to a timestamp"""
    match = re.search(
        r'(?i)(\d+)\s*(year|month|week|day|hour|minute|second|min|sec)s?', time_text)
    if match:
        # time unit: time value
        kwargs = {f'{match.group(2).lower()}s': int(match.group(1))}
        return (datetime.now() - relativedelta(**kwargs)).strftime('%Y-%m-%d %H:%M:%S')
    try:
        return parse(time_text, fuzzy=True).strftime('%Y-%m-%d %H:%M:%S')
    except ParserError:
        print(f"Could not parse publish time: {time_text}")
