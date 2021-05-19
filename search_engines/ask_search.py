from search_engines.utils import extract_first
from lxml.html import fromstring

from typing import Dict, List, Tuple
from urllib.parse import quote


def extract_search_results(html: str, page_url: str) -> Tuple[List[Dict[str, str]], str]:
    root = fromstring(html)
    page_number = extract_first(root.xpath(
        '//li[@class="PartialWebPagination-condensed PartialWebPagination-pgsel PartialWebPagination-button"]/text()'))
    results = [
        {
            'url': extract_first(result.xpath('.//a[@class="PartialSearchResults-item-title-link result-link"]/@href')),
            'title': extract_first(result.xpath('.//a[@class="PartialSearchResults-item-title-link result-link"]/text()')),
            'preview_text': extract_first(result.xpath('.//p[@class="PartialSearchResults-item-abstract"]/text()')),
            'page_number': page_number or "1",
        } for result in root.xpath('//div[@class="PartialSearchResults-item"]')]
    next_page_url = extract_first(
        root.xpath('//li[@class="PartialWebPagination-next"]/parent::a/@href'))
    if next_page_url:
        next_page_url = 'https://www.ask.com' + next_page_url
    return results, next_page_url


def get_search_url(query: str, latest: bool, country: str):
    return f'https://www.ask.com/web?q={quote(query)}'
