from search_engines.utils import extract_first, join_all
from lxml.html import fromstring

from typing import Dict, List, Tuple
from urllib.parse import quote


async def extract_search_results(html: str, search_url: str) -> Tuple[List[Dict[str, str]], str]:
    root = fromstring(html)
    page_number = extract_first(root.xpath(
        '//*[@role="navigation"]//tr/td[@class="YyVfkd"]/text()'))
    results = [
        {
            'url': extract_first(result.xpath("./a/@href")),
            'title': join_all(result.xpath("./a/h3/text()")),
            'preview_text': join_all(result.xpath("./following-sibling::*[@class='s']//*[@class='st']//test()")),
            'search_url': search_url,
            'page_number': page_number,
        } for result in root.xpath('//*[@class="r"]')]
    print(
        f"Extracted {len(results)} results from page {page_number}.")
    next_page_url = extract_first(root.xpath('//a[@id="pnnext"]/@href'))
    if next_page_url:
        next_page_url = 'https://www.google.com' + next_page_url
        print(f"Extracted next page url: {next_page_url}")
    else:
        print(f"No next page url found: {search_url}")
    return results, next_page_url


def search_url(query: str):
    return f"https://www.google.com/search?q={quote(query)}"
