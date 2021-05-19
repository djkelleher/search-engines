from search_engines.utils import extract_first, join_all, publish_time
from lxml.html import fromstring

from typing import Dict, List, Tuple
from urllib.parse import quote


def extract_search_results(html: str, page_url: str) -> Tuple[List[Dict[str, str]], str]:
    root = fromstring(html)
    page_number = extract_first(
        root.xpath('//div[@class="compPagination"]//strong/text()'))
    results = [
        {
            'url': extract_first(result.xpath('.//a[@title]/@href')),
            'title': extract_first(result.xpath('.//a[@title]/@title')),
            'preview_text': join_all(result.xpath("//div[@class='compText aAbs']//text()")),
            'publisher': extract_first(result.xpath('.//span[contains(@class,"mr-5 cite-co")]/text()')),
            'publish_date': publish_time(extract_first(result.xpath('.//span[contains(@class,"s-time")]/text()'))),
            'page_number': page_number,
        } for result in root.xpath('//ol[contains(@class,"searchCenterMiddle")]/li')]
    next_page_url = extract_first(root.xpath('//a[@class="next"]/@href'))
    return results, next_page_url


def get_search_url(query: str):
    return f'https://news.search.yahoo.com/search?p={quote(query)}&fr=uh3_news_vert_gs'
