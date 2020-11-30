from search_engines.utils import extract_first, join_all, publish_date_from_time
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
            'title': join_all(result.xpath("./a//div[@role='heading']/text()")),
            'preview_text': join_all(result.xpath(".//div[@class='dbsr']/a//div[@class='eYN3rb']/text()")),
            'publisher': extract_first(result.xpath('./a//div[@class="pDavDe RGRr8e"]/text()')),
            'publish_date': publish_date_from_time(extract_first(result.xpath('.//span[@class="eNg7of"]/span/text()'))),
            'search_url': search_url,
            'page_number': page_number,
        } for result in root.xpath('//div[@class="dbsr"]')]
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
    # TODO shorten this
    return f'https://www.google.com/search?q={quote(query)}&sxsrf=ALeKk02Xj0vvvwQayorVgMTEjV8IHSgj4w:1586286484301&source=lnms&tbm=nws&sa=X&ved=2ahUKEwj_mKLTgdfoAhV3knIEHWi0A8IQ_AUoAXoECBkQAw&biw=1359&bih=981'
