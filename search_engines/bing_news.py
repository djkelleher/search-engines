from search_engines.utils import encode_url_str, extract_first, get_logger, get_publish_time, http_search
from lxml.html import fromstring
from pathlib import Path
from aiohttp.client import ClientSession
from aiohttp.client_reqrep import ClientResponse
from typing import Dict, Tuple, List
import re

log_save_path = Path(__file__).parent.joinpath('logs/bing_news.log')
logger = get_logger("Bing News", log_save_path)


async def parse_page(resp: ClientResponse,
                     query: str) -> Tuple[List[Dict[str, str]], str]:
    html = await resp.text()
    root = fromstring(html)
    results = []
    for result in root.xpath(
            '//div[@class="news-card newsitem cardcommon b_cards2"]'):
        publish_time = extract_first(
            result.xpath('.//div[@class="source"]//span/@aria-label'))
        date_match = re.search(r'\d{1,2}\/\d{1,2}\/\d{4}', publish_time)
        if date_match:
            publish_date = date_match.group()
        else:
            publish_date = get_publish_time(publish_time)
        results.append({
            'query':
            query,
            'url':
            extract_first(result.xpath('.//a[@class="title"]/@href')),
            'title':
            extract_first(result.xpath('.//a[@class="title"]/text()')),
            'preview_text':
            extract_first(result.xpath('.//div[@class="snippet"]/@title')),
            'publisher':
            extract_first(
                result.xpath(
                    './/div[@class="source"]//a[@aria-label]/text()')),
            'publish_date':
            publish_date,
            'page_url':
            str(resp.url),
            'source':
            "Bing News"
        })
    logger.info(f"Extracted {len(results)} search results for query: {query}")
    return results, None  # no next page url.


async def do_search(client: ClientSession,
                    query: str,
                    headers: Dict[str, str],
                    page_min_sleep: int = 0,
                    page_max_sleep: int = 0,
                    max_pages: int = 1000):
    start_url = 'https://www.bing.com/news/search?q=' + encode_url_str(query)
    return await http_search(client=client,
                             query=query,
                             page_url=start_url,
                             headers=headers,
                             parse_page_cb=parse_page,
                             page_min_sleep=page_min_sleep,
                             page_max_sleep=page_max_sleep,
                             max_pages=max_pages)
