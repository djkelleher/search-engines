from search_engines.utils import extract_first, join_all, publish_time
from lxml.html import fromstring
from typing import Dict, List, Tuple
from urllib.parse import quote
import re


def extract_search_results(html: str) -> Tuple[List[Dict[str, str]], str]:
    root = fromstring(html)
    results = []
    for result in root.xpath('//div[@class="news-card newsitem cardcommon b_cards2"]'):
        pub_time = extract_first(
            result.xpath('.//div[@class="source"]//span/@aria-label'))
        publish_date = re.search(r'\d{1,2}\/\d{1,2}\/\d{4}', pub_time)
        results.append({
            'url': extract_first(result.xpath('.//a[@class="title"]/@href')),
            'title': extract_first(result.xpath('.//a[@class="title"]/text()')),
            'preview_text': extract_first(result.xpath('.//div[@class="snippet"]/@title')),
            'publisher': extract_first(result.xpath('.//div[@class="source"]//a[@aria-label]/text()')),
            'publish_date': publish_date.group() if publish_date else publish_time(pub_time),
            'page_number': "1",
        })
    """
    next_page_url = extract_first(root.xpath("//a[@title='Next page']/@href"))
    if next_page_url:
        next_page_url = 'https://www.bing.com' + next_page_url
    """
    # now a single page. need to scroll to load all content.
    return results, None


def get_search_url(query: str):
    return f'https://www.bing.com/news/search?q={quote(query)}'
