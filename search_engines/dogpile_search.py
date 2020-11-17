from search_all.utils import extract_first, join_all, logger, publish_date_from_time
from lxml.html import fromstring

from typing import Dict, List, Tuple
from urllib.parse import quote


async def extract_search_results(html: str, search_url: str) -> Tuple[List[Dict[str, str]], str]:
    root = fromstring(html)
    page_number = extract_first(root.xpath(
        '//span[@class="pagination__num pagination__num--active"]/text()'))
    results = [
        {
            'url': extract_first(result.xpath('.//a[@class="web-bing__title"]/@href')),
            'title': extract_first(result.xpath('.//a[@class="web-bing__title"]/text()')),
            'preview_text': extract_first(result.xpath('.//span[@class="web-bing__description"]/text()')),
            'search_url': search_url,
            'page_number': page_number,
        } for result in root.xpath('//div[@class="web-bing__result"]')]
    logger.info(
        f"Extracted {len(results)} results from page {page_number}.")
    next_page_url = extract_first(root.xpath(
        '//a[@class="pagination__num pagination__num--next-prev pagination__num--next"]/@href'))
    if next_page_url:
        next_page_url = 'https://www.dogpile.com' + next_page_url
        logger.info(f"Extracted next page url: {next_page_url}")
    else:
        logger.info(f"No next page url found: {search_url}")
    return results, next_page_url


def search_url(query: str):
    return f'https://www.dogpile.com/serp?qc=web&q={quote(query)}'
