from distbot.spider import Spider
import search_engines as se
import asyncio


engines = (se.ask_search,
           se.bing_news,
           se.bing_search,
           se.dogpile_news,
           se.dogpile_search,
           se.google_news,
           se.google_search,
           se.yahoo_news,
           se.yahoo_search)


spider = None


async def search_all(query: str, max_pages: int):
    tasks, all_results = [], []

    async def search(url, engine, max_pages, page_num=1):
        _, page = await spider.get(url)
        await asyncio.sleep(0.1)
        html = await page.content()
        await spider.set_idle(page)
        results, url = await engine.extract_search_results(html, url)
        all_results += results
        if url and page_num < max_pages:
            page_num += 1
            tasks.append(
                asyncio.create_task(
                    search(url, engine, max_pages, page_num)))
    for e in engines:
        url = e.search_url(query)
        tasks.append(
            asyncio.create_task(
                search(url, e, max_pages)))
    await asyncio.gather(*tasks)
    return all_results


async def get_spider(browsers: int = 1):
    spider = Spider()
    for _ in range(browsers):
        await spider.add_browser(launch_options={
            "headless": False,
            "ignoreHTTPSErrors": True,
            "defaultViewport": {},
            "executablePath": "/usr/bin/google-chrome-stable",
            # "userDataDir": "/home/dan/Default",
            "defaultNavigationTimeout": 60_000,
            "args": [
                "--disable-web-security",
                "--no-sandbox",
                "--start-maximized",
                # "--blink-settings=imagesEnabled=false",
            ]
        })
    return spider


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a',
                        '--address',
                        type=str,
                        default='0.0.0.0',
                        help='Address to run the server on.')
    parser.add_argument('-p',
                        '--port',
                        type=int,
                        default='80',
                        help='Port to run the server on.')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    app.run(host=args.address, port=args.port)
