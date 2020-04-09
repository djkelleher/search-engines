from search_engines.utils import encode_url_str, extract_first, get_logger, http_search
from lxml.html import fromstring
from pathlib import Path
from aiohttp.client import ClientSession
from aiohttp.client_reqrep import ClientResponse
from typing import Dict, Tuple, List

log_save_path = Path(__file__).parent.joinpath('logs/ask_search.log')
logger = get_logger("Ask Search", log_save_path)

async def parse_page(resp: ClientResponse, query: str) -> Tuple[List[Dict[str,str]],str]:
    html = await resp.text()
    root = fromstring(html)
    page_num = extract_first(root.xpath('//li[@class="PartialWebPagination-condensed PartialWebPagination-pgsel PartialWebPagination-button"]/text()'))
    page_url = str(resp.url)
    results = [{
        'url': extract_first(result.xpath('.//a[@class="PartialSearchResults-item-title-link result-link"]/@href')),
        'title': extract_first(result.xpath('.//a[@class="PartialSearchResults-item-title-link result-link"]/text()')),
        'preview_text': extract_first(result.xpath('.//p[@class="PartialSearchResults-item-abstract"]/text()')),
        'page_url': page_url,
        'page_num': page_num if page_num else "1",
        'query': query,
        'source': "Ask"}
        for result in root.xpath('//div[@class="PartialSearchResults-item"]')]
    logger.info(f"Extracted {len(results)} results from page {page_num}. Query: {query}")
    next_page_url = extract_first(root.xpath('//li[@class="PartialWebPagination-next"]/parent::a/@href'))
    if next_page_url:
        next_page_url = 'https://www.ask.com'+next_page_url
        logger.info(f"Extracted next page url: {next_page_url}")
    else:
        logger.info(f"No next page url found: {page_url}")
    return results, next_page_url

async def do_search(client: ClientSession, query: str, headers: Dict[str,str],
                    page_min_sleep: int = 0, page_max_sleep: int = 0,
                    max_pages: int = 1000):
    start_url = 'https://www.ask.com/web?q='+encode_url_str(query)
    return await http_search(client=client,
                            query=query,
                            page_url=start_url,
                            headers=headers,
                            parse_page_cb=parse_page,
                            page_min_sleep=page_min_sleep,
                            page_max_sleep=page_max_sleep,
                            max_pages=max_pages)