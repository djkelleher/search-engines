from search_engines.utils import extract_first, join_all, publish_date_from_time
from lxml.html import fromstring

from typing import Dict, List, Tuple
from urllib.parse import quote


async def extract_search_results(html: str, search_url: str) -> Tuple[List[Dict[str, str]], str]:
    root = fromstring(html)
    page_number = extract_first(root.xpath(
        '//div[@class="compPagination"]/strong/text()'))
    results = []
    for result in root.xpath('//ol[contains(@class,"searchCenterMiddle")]/li'):
        url = extract_first(result.xpath(
            ".//h3[contains(@class,'title')]//a/@href"))
        if url and 'news.search.yahoo' not in url and 'video.search.yahoo' not in url:
            results.append({
                'url': url,
                'title': join_all(result.xpath(".//h3[contains(@class,'title')]//a//text()")),
                'preview_text': join_all(result.xpath(".//div[@class='compText aAbs']//text()")),
                'search_url': search_url,
                'page_number': page_number,
            })
    print(
        f"Extracted {len(results)} results from page {page_number}.")
    next_page_url = extract_first(root.xpath("//*[@class='next']/@href"))
    if next_page_url:
        print(f"Extracted next page url: {next_page_url}")
    else:
        print(f"No next page url found: {search_url}")
    return results, next_page_url


def search_url(query: str):
    return f'https://search.yahoo.com/search?p={quote(query)}'
