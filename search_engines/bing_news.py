from search_engines.utils import extract_first, publish_time
from lxml.html import fromstring
from typing import Dict, List, Tuple
from urllib.parse import quote, urlsplit, parse_qs
import re


def extract_search_results(
    html: str, page_url: str
) -> Tuple[List[Dict[str, str]], str]:
    root = fromstring(html)
    results = []
    params = dict(parse_qs(urlsplit(page_url).query))
    current_page = str(int(((int(params["first"][0]) - 1) / 10) + 1))

    for result in root.xpath('//div[@class="news-card newsitem cardcommon b_cards2"]'):
        pub_time = extract_first(
            result.xpath('.//div[@class="source"]//span/@aria-label')
        )
        publish_date = re.search(r"\d{1,2}\/\d{1,2}\/\d{4}", pub_time)
        results.append(
            {
                "url": extract_first(result.xpath('.//a[@class="title"]/@href')),
                "title": extract_first(result.xpath('.//a[@class="title"]/text()')),
                "preview_text": extract_first(
                    result.xpath('.//div[@class="snippet"]/@title')
                ),
                "publisher": extract_first(
                    result.xpath('.//div[@class="source"]//a[@aria-label]/text()')
                ),
                "publish_date": publish_date.group()
                if publish_date
                else publish_time(pub_time),
                "page_number": current_page,
            }
        )

    next_page_url = (
        f'https://www.bing.com/news/infinitescrollajax?q={quote(params["q"][0])}&InfiniteScroll=1&first='
        + str(int(params["first"][0]) + 10)
    )

    return results, next_page_url


def get_search_url(query: str, latest: bool = True, country: str = "us") -> str:
    url = f"https://www.bing.com/news/infinitescrollajax?q={quote(query)}&InfiniteScroll=1&first=1"
    if latest:
        url += "&qft=sortbydate" + quote('="1"')

    return url
