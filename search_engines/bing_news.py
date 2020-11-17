from search_all.utils import extract_first, join_all, encode_url_str, logger, publish_date_from_time
from lxml.html import fromstring
from typing import Dict, List, Tuple
import re


async def extract_search_results(html: str, search_url: str) -> Tuple[List[Dict[str, str]], str]:
    root = fromstring(html)
    page_number = extract_first(
        root.xpath('//a[@class="sb_pagS sb_pagS_bp b_widePag sb_bp"]/text()'))
    results = []
    for r in root.xpath('//div[@class="news-card newsitem cardcommon b_cards2"]'):
        publish_time = extract_first(
            r.xpath('.//div[@class="source"]//span/@aria-label'))
        publish_date = re.search(r'\d{1,2}\/\d{1,2}\/\d{4}', publish_time)
        results.append({
            'url': extract_first(r.xpath('.//a[@class="title"]/@href')),
            'title': extract_first(r.xpath('.//a[@class="title"]/text()')),
            'preview_text': extract_first(r.xpath('.//div[@class="snippet"]/@title')),
            'publisher': extract_first(r.xpath('.//div[@class="source"]//a[@aria-label]/text()')),
            'publish_date': publish_date.group() if publish_date else publish_date_from_time(publish_time),
            'search_url': search_url,
            'page_number': page_number,
        })
    next_page_url = extract_first(root.xpath("//a[@title='Next page']/@href"))
    if next_page_url:
        next_page_url = 'https://www.bing.com' + next_page_url
        logger.info(f"Extracted next page url: {next_page_url}")
    else:
        logger.info(f"No next page url found: {search_url}")
    return results, next_page_url


def search_url(query: str):
    return 'https://www.bing.com/news/search?q=' + encode_url_str(query)
