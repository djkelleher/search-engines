from search_engines.utils import encode_url_str, extract_first, join_all, get_logger, get_publish_time, http_search
from lxml.html import fromstring
from pathlib import Path
from aiohttp.client import ClientSession
from aiohttp.client_reqrep import ClientResponse
from typing import Dict, Tuple, List

log_save_path = Path(__file__).parent.joinpath('logs/google_news.log')
logger = get_logger("Google News", log_save_path)

async def parse_page(resp: ClientResponse, query: str) -> Tuple[List[Dict[str,str]],str]:
    html = await resp.text()
    root = fromstring(html)
    page_num = extract_first(root.xpath('//*[@role="navigation"]//tr/td[@class="YyVfkd"]/text()'))
    page_url = str(resp.url)
    results = [{
            'url': extract_first(result.xpath("./a/@href")),
            'title': join_all(result.xpath("./a//div[@role='heading']/text()")),
            'preview_text': join_all(result.xpath(".//div[@class='dbsr']/a//div[@class='eYN3rb']/text()")),
            'publisher': extract_first(result.xpath('./a//div[@class="pDavDe RGRr8e"]/text()')),
            'publish_date': get_publish_time(extract_first(result.xpath('.//span[@class="eNg7of"]/span/text()'))),
            'page_url': page_url,
            'page_num': page_num,
            'query': query,
            'source': "Google News"}
            for result in root.xpath('//div[@class="dbsr"]')]
    logger.info(f"Extracted {len(results)} results from page {page_num}. Query: {query}")
    next_page_url = extract_first(root.xpath('//a[@id="pnnext"]/@href'))
    if next_page_url:
        next_page_url = 'https://www.google.com'+next_page_url
        logger.info(f"Extracted next page url: {next_page_url}")
    else:
        logger.info(f"No next page url found: {page_url}")
    return results, next_page_url

async def do_search(client: ClientSession, query: str, headers: Dict[str,str],
                    page_min_sleep: int = 0, page_max_sleep: int = 0,
                    max_pages: int = 1000):
    start_url = f'https://www.google.com/search?q={encode_url_str(query)}&sxsrf=ALeKk02Xj0vvvwQayorVgMTEjV8IHSgj4w:1586286484301&source=lnms&tbm=nws&sa=X&ved=2ahUKEwj_mKLTgdfoAhV3knIEHWi0A8IQ_AUoAXoECBkQAw&biw=1359&bih=981'
    return await http_search(client=client,
                            query=query,
                            page_url=start_url,
                            headers=headers,
                            parse_page_cb=parse_page,
                            page_min_sleep=page_min_sleep,
                            page_max_sleep=page_max_sleep,
                            max_pages=max_pages)