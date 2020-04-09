from search_engines import ask_search, bing_news, bing_search, dogpile_news, dogpile_search, google_news, google_search, yahoo_news, yahoo_search
from aiohttp.client import ClientSession
from typing import List, Dict
from pathlib import Path
import inspect
import asyncio
import json

headers = {
    "user-agent":
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

sources = {
    'ask': ask_search,
    'bing news': bing_news,
    'bing': bing_search,
    'dogpile news': dogpile_news,
    'dogpile': dogpile_search,
    'google news': google_news,
    'google': google_search,
    'yahoo news': yahoo_news,
    'yahoo': yahoo_search
}


async def search(source: str,
                 query: str,
                 max_pages: int = 1000,
                 page_min_sleep: int = 0,
                 page_max_sleep: int = 0) -> List[Dict[str, str]]:
    module = sources.get(source.lower())
    if not module:
        raise ValueError(
            f"Invaid source: {source}. Valid source are: {', '.join([sources.keys()])}"
        )
    async with ClientSession() as client:
        return await module.do_search(client=client,
                                      query=query,
                                      headers=headers,
                                      max_pages=max_pages,
                                      page_min_sleep=page_min_sleep,
                                      page_max_sleep=page_max_sleep)
