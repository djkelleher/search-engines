from search_all.utils import extract_first, join_all, logger, publish_date_from_time
from lxml.html import fromstring

from typing import Dict, List, Tuple
from urllib.parse import quote


async def extract_search_results(html: str, search_url: str) -> Tuple[List[Dict[str, str]], str]:
    root = fromstring(html)
    page_number = extract_first(
        root.xpath('//div[@class="compPagination"]//strong/text()'))
    results = [
        {
            'url': extract_first(result.xpath('.//a[@title]/@href')),
            'title': extract_first(result.xpath('.//a[@title]/@title')),
            'preview_text': join_all(result.xpath("//div[@class='compText aAbs']//text()")),
            'publisher': extract_first(result.xpath('.//a[@title]/following-sibling::span[@class="mr-5 cite-co"]/text()')),
            'publish_date': publish_date_from_time(extract_first(result.xpath('.//a[@title]/following-sibling::span[@class="fc-2nd mr-8"]/text()'))),
            'search_url': search_url,
            'page_number': page_number,
        } for result in root.xpath('//ol[contains(@class,"searchCenterMiddle")]/li')]
    logger.info(
        f"Extracted {len(results)} results from page {page_number}.")
    next_page_url = extract_first(root.xpath('//a[@class="next"]/@href'))
    if next_page_url:
        logger.info(f"Extracted next page url: {next_page_url}")
    else:
        logger.info(f"No next page url found: {search_url}")
    return results, next_page_url


def search_url(query: str):
    return f'https://news.search.yahoo.com/search?p={quote(query)}&fr=uh3_news_vert_gs'
