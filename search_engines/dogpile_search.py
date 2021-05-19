from search_engines.utils import extract_first, join_all
from lxml.html import fromstring

from typing import Dict, List, Tuple
from urllib.parse import quote


def extract_search_results(html: str, page_url: str) -> Tuple[List[Dict[str, str]], str]:
    root = fromstring(html)
    page_number = extract_first(root.xpath(
        '//span[@class="pagination__num pagination__num--active"]/text()'))
    results = [
        {
            'url': extract_first(result.xpath('.//a[@class="web-bing__title"]/@href')),
            'title': join_all(result.xpath('.//a[@class="web-bing__title"]//text()')),
            'preview_text': join_all(result.xpath('.//span[@class="web-bing__description"]//text()')),
            'page_number': page_number,
        } for result in root.xpath('//div[@class="web-bing__result"]')]
    next_page_url = extract_first(root.xpath(
        '//a[@class="pagination__num pagination__num--next-prev pagination__num--next"]/@href'))
    if next_page_url:
        next_page_url = 'https://www.dogpile.com' + next_page_url
    return results, next_page_url


def get_search_url(query: str, latest: bool, country: str):
    return f'https://www.dogpile.com/serp?qc=web&q={quote(query)}'
