from search_engines.utils import extract_first, join_all, encode_url_str, get_logger, http_search 
from lxml.html import fromstring
from aiohttp.client_reqrep import ClientResponse
from aiohttp.client import ClientSession
from typing import Dict, List, Tuple
from pathlib import Path


log_save_path = Path(__file__).parent.joinpath('logs/bing_search.log')
logger = get_logger("Bing Search", log_save_path)

async def parse_page(resp: ClientResponse, query: str) -> Tuple[List[Dict[str,str]],str]:
    html = await resp.text()
    root = fromstring(html)
    page_num = extract_first(root.xpath('//a[@class="sb_pagS sb_pagS_bp b_widePag sb_bp"]/text()'))
    page_url = str(resp.url)
    results = [{
        'query': query,
        'url': extract_first(result.xpath("./h2/a/@href")),
        'title': join_all(result.xpath("./h2/a//text()")),
        'preview_text': join_all(result.xpath("./*[@class='b_caption']/p//text()")),
        'page_url': page_url,
        'page_num': page_num,
        'source': "Bing"}
        for result in root.xpath("//*[@class='b_algo']")]
    logger.info(f"Extracted {len(results)} results from page {page_num}. Query: {query}")
    # extract url of next page.
    next_page_url = extract_first(root.xpath("//a[@title='Next page']/@href"))
    if next_page_url:
        next_page_url = 'https://www.bing.com'+next_page_url
        logger.info(f"Extracted next page url: {next_page_url}")
    else:
        logger.info(f"No next page url found: {page_url}")
    return results, next_page_url

async def do_search(client: ClientSession, query: str, headers: Dict[str,str],
                    page_min_sleep: int = 0, page_max_sleep: int = 0,
                    max_pages: int = 1000):
    start_url = 'https://www.bing.com/search?q='+encode_url_str(query)
    return await http_search(client=client,
                            query=query,
                            page_url=start_url,
                            headers=headers,
                            parse_page_cb=parse_page,
                            page_min_sleep=page_min_sleep,
                            page_max_sleep=page_max_sleep,
                            max_pages=max_pages)