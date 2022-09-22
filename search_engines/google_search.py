from search_engines.utils import extract_first, join_all
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
    results = []
    for result in root.xpath('//*[@class="g"]'):
        url_ele = result.xpath(".//a[@data-ved][@ping]")
        if len(url_ele):
            url_ele = url_ele[0]
            results.append(
                {
                    "url": extract_first(url_ele.xpath("./@href")),
                    "title": extract_first(url_ele.xpath("./h3/text()")),
                    "preview_text": join_all(
                        result.xpath('.//span[@class="aCOpRe"]//text()')
                    ),
                    "page_number": page_number,
                }
            )
    next_page_url = extract_first(root.xpath('//a[@id="pnnext"]/@href'))
    if next_page_url:
        next_page_url = "https://www.google.com" + next_page_url
    return results, next_page_url


def get_search_url(query: str, latest: bool = True, country: str = "us") -> str:
    return f"https://www.google.com/search?q={quote(query)}"
