## Description
Query and scrape search engines (Google, Google News, Yahoo, Yahoo News, Bing, Bing News, Ask, Dogpile, Dogpile News)   

## Installation
`pip install search_engines`   

## Usage
API has one function:   

`search(source: str, query: str, max_pages: int = 1000,
        page_min_sleep: int = 0, page_max_sleep: int = 0) -> List[Dict[str,str]]`   

Returned dictionaries will have keys: 'url', 'title', 'preview_text', 'page_url', 'page_num', 'query', 'source'.   
If *source* argument is a news source, returned dictionaries will have additional keys 'publisher' and 'publish_date'.   

Valid arguments for *source* are: 'ask', 'bing news', 'bing', 'dogpile news', 'dogpile', 'google news', 'google', 'yahoo news', 'yahoo'     

After scraping a results page, the spider will sleep for a random time between *page_min_sleep* and *page_max_sleep* before proceeding to the next page.   

## Example
```
from search_engines.search import search

query = "coronavirus"
source = "bing"
max_pages = "5"

results = await search(source, query, max_pages)
```