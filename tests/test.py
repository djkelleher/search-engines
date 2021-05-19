from pathlib import Path
from pyppeteer import launch
from pprint import pformat
import pyppeteer_stealth
import asyncio
import json

from search_engines import (ask_search,
                            bing_news,
                            bing_search,
                            dogpile_news,
                            dogpile_search,
                            google_news,
                            google_search,
                            yahoo_news,
                            yahoo_search)

modules = {
    'ask_search': ask_search,
    'bing_news': bing_news,
    'bing_search': bing_search,
    'dogpile_search': dogpile_search,
    'dogpile_news': dogpile_news,
    'google_news': google_news,
    'google_search': google_search,
    'yahoo_news': yahoo_news,
    'yahoo_search': yahoo_search,
}


async def open_browser():
    launch_options = {
        "headless": False,
        "ignoreHTTPSErrors": True,
        "defaultViewport": {},
        "args": [
            "--disable-web-security",
            "--no-sandbox",
            "--start-maximized",
        ],
    }
    # Prefer Chrome over Chromium.
    if Path('/usr/bin/google-chrome-stable').is_file():
        launch_options['executablePath'] = '/usr/bin/google-chrome-stable'
    elif Path('/bin/google-chrome-stable').is_file():
        launch_options['executablePath'] = '/bin/google-chrome-stable'
    browser = await launch(launch_options)
    # browser opens with one page by default.
    pages = await browser.pages()
    page = pages.pop()
    await pyppeteer_stealth.stealth(
        page,
        run_on_insecure_origins=True,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        locale="en-US,en",
        # TCP fingerprinting can detect Linux is masked (e.g. from TTL value), so don't set True
        mask_linux=False,
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
    )
    await page._client.send('Network.setBlockedURLs', {'urls': [
        "adssettings.google.com",
        "doubleclick.net",
        "googlesyndication.com",
        "google.com/ads",
        "securepubads.g.doubleclick.net",
        "ads.pubmatic.com",
        "adservice.google.com",
        "amazon-adsystem.com"
        "google-analytics.com"
        "googletagmanager.com"
    ]})
    return browser, page


async def test_search(query):
    browser, page = await open_browser()
    for name, module in modules.items():
        print(f"Starting {name}")
        url = module.get_search_url(query=query, latest=True, country='US')
        all_results = []
        for i in range(4):
            await page.goto(url)
            html = await page.content()
            results, url = module.extract_search_results(
                html=html, page_url=url)
            print(f"{name} page {i}:\n{pformat(results)}")
            print(f"Next page URL: {url}")
            all_results.append(results)
            await asyncio.sleep(2)
        results_dir.joinpath(f'{name}.json').write_text(
            json.dumps(all_results, indent=4))
    await browser.close()


if __name__ == '__main__':
    import sys

    results_dir = Path(__file__).parent / "search_results"
    results_dir.mkdir(exist_ok=True)

    query = sys.argv[1] if len(sys.argv) > 1 else "Tesla TSLA"
    print(f"Query: {query}")

    asyncio.run(test_search(query))
