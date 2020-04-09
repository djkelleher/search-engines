from aiohttp.client import ClientSession
from aiohttp.client_reqrep import ClientResponse
from pyppeteer_spider.spider import PyppeteerSpider
from pyppeteer.page import Page
from typing import Dict, List, Callable, Tuple
from urllib.parse import urlsplit, urlunsplit
from datetime import datetime, timedelta
from pathlib import Path
import logging.handlers
import logging
import random
import asyncio
import re

char_to_formatter = {
    " ": "+",
    ":": "%3A",
    ";": "%3B",
    "'": "%27",
    "!": "%21",
    "`": "%60",
    "@": "%40",
    "#": "%23",
    "$": "%24",
    "%": "%25",
    "^": "%5E",
    "&": "%26",
    "(": "%28",
    ")": "%29",
    "+": "%2B",
    "=": "%3D",
    "?": "%3F",
    "/": "%2F",
    "\\": "%5C",
    "|": "%7C",
    "[": "%5B",
    "]": "%5D",
    "{": "%7B",
    "}": "%7D"
}


def encode_url_str(url_str):
    to_format = [(char, formatter)
                 for char, formatter in char_to_formatter.items()
                 if char in url_str]
    for char, formatter in to_format:
        url_str = url_str.replace(char, formatter)
    return url_str


def extract_first(query_result):
    return str(query_result[0]).strip() if len(query_result) > 0 else ""


def extract_all(query_result):
    return [str(res).strip() for res in query_result]


def join_all(query_result, join_str=" "):
    return join_str.join([str(t).strip() for t in query_result
                          ]) if len(query_result) > 0 else ""


def get_publish_time(time_published_text):
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


def get_logger(logger_name, log_save_path=None, log_level=logging.INFO):
    logging.basicConfig(
        format='[%(name)s][%(levelname)s][%(asctime)s] %(message)s',
        level=log_level)
    logger = logging.getLogger(logger_name)
    if log_save_path is not None:
        log_save_path = Path(log_save_path)
        if not log_save_path.parent.is_dir():
            try:
                log_save_path.parent.mkdir(exist_ok=True, parents=True)
            except (FileNotFoundError, PermissionError) as e:
                logger.error(
                    f"Error creating log directory '{log_save_path.parent}'. No log will be saved. Error: {e}"
                )
                return logger
        logger.info(f"Using log_save_path '{log_save_path}'")
        fh = logging.handlers.RotatingFileHandler(log_save_path,
                                                  maxBytes=10_000_000,
                                                  backupCount=2)
        logger.addHandler(fh)
    return logger


async def http_search(client: ClientSession,
                      query: str,
                      page_url: str,
                      headers: Dict[str, str],
                      parse_page_cb: Callable[[ClientResponse, str],
                                              Tuple[List[Dict[str, str]],
                                                    str]],
                      page_min_sleep: int = 0,
                      page_max_sleep: int = 0,
                      max_pages: int = 1000) -> List[Dict[str, str]]:
    print(f"Starting search query: {query}. Start url: {page_url}")
    all_results = []
    for i in range(int(max_pages)):
        resp = await client.get(page_url)
        print(f"[{resp.status}] {page_url}")
        results, page_url = await parse_page_cb(resp, query)
        all_results += results
        if page_url:
            await asyncio.sleep(random.uniform(page_min_sleep, page_max_sleep))
        else:
            print(f"""Next page not found. Processed {i+1} total results pages.
                            Returning {len(all_results)} total results.""")
            return all_results
    print(f"""Finished search '{query}'. Processed {i+1} total results pages.
                Returning {len(all_results)} total results.""")
    return all_results


async def browser_search(query: str,
                         page_url: str,
                         parse_page_cb: Callable[[Page, str],
                                                 Tuple[List[Dict[str, str]],
                                                       str]],
                         page_min_sleep: int = 0,
                         page_max_sleep: int = 0,
                         max_pages: int = 1000):
    spider = await PyppeteerSpider().launch()
    print(f"Starting search query: {query}. Start url: {page_url}")
    all_results = []
    for i in range(max_pages):
        page = await spider.get(page_url)
        results, page_url = await parse_page_cb(page, query)
        await spider.set_idle(page)
        all_results += results
        if page_url:
            await asyncio.sleep(random.uniform(page_min_sleep, page_max_sleep))
        else:
            print(f"Next page not found.")
            break
    await spider.shutdown()
    print(f"""Finished search '{query}'. Processed {i+1} total results pages.
                    Returning {len(all_results)} total results.""")
    return all_results
