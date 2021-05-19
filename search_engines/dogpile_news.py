from search_engines.utils import extract_first
from lxml.html import fromstring

from typing import Dict, List, Tuple
from urllib.parse import quote


def extract_search_results(html: str, page_url: str) -> Tuple[List[Dict[str, str]], str]:
    root = fromstring(html)
    page_number = extract_first(root.xpath(
        '//span[@class="pagination__num pagination__num--active"]/text()'))
    results = []
    for result in root.xpath('//p[@class="article"]'):
        pushlish_info = extract_first(result.xpath(
            './/*[@class="source"]/text()')).split(",")
        publisher = pushlish_info.pop(0).strip() if len(pushlish_info) else ""
        publish_date = pushlish_info.pop(
            0).strip() if len(pushlish_info) else ""
        results.append({
            'url': extract_first(result.xpath('./a/@href')),
            'title': extract_first(result.xpath('./a/*[@class="title"]/text()')),
            'preview_text': extract_first(result.xpath('./span[@class="description"]/text()')),
            'publisher': publisher,
            'publish_date': publish_date,
            'page_number': page_number,
        })
    next_page_url = extract_first(root.xpath(
        '//a[@class="pagination__num pagination__num--next-prev pagination__num--next"]/@href'))
    if next_page_url:
        next_page_url = 'https://www.dogpile.com' + next_page_url
    return results, next_page_url


def get_search_url(query: str):
    f'https://www.dogpile.com/serp?qc=news&q={quote(query)}'
