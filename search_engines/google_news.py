from search_engines.utils import extract_first, join_all, publish_time
from lxml.html import fromstring

from typing import Dict, List, Tuple
from urllib.parse import quote


def extract_search_results(
    html: str, page_url: str
) -> Tuple[List[Dict[str, str]], str]:
    root = fromstring(html)
    page_number = extract_first(
        root.xpath('//*[@role="navigation"]//tr/td[@class="YyVfkd"]/text()')
    )
    results = [
        {
            "url": extract_first(result.xpath("./a/@href")),
            "title": join_all(result.xpath("./a//div[@role='heading']/text()")),
            "preview_text": join_all(result.xpath('.//div[@class="Y3v8qd"]/text()')),
            "publisher": extract_first(
                result.xpath('.//div[@class="XTjFC WF4CUc"]/text()')
            ),
            "publish_date": publish_time(
                extract_first(result.xpath('.//span[@class="WG9SHc"]/span/text()'))
            ),
            "page_number": page_number,
        }
        for result in root.xpath('//div[@class="dbsr"]')
    ]
    next_page_url = extract_first(root.xpath('//a[@id="pnnext"]/@href'))
    if next_page_url:
        next_page_url = "https://www.google.com" + next_page_url
    return results, next_page_url


def get_search_url(query: str, latest: bool = True, country: str = "us") -> str:
    url = f"https://www.google.com/search?q={quote(query)}&tbm=nws"
    if latest:
        url += "&tbs=sbd:1"

    return url
