
### **Query and scrape search engines (Google, Google News, Yahoo, Yahoo News, Bing, Bing News, Ask, Dogpile, Dogpile News)**
----
## Installation
```pip install search_engines```   

## Overview
Each search engine has a module {engine_name}.py which two functions:   
```python 
extract_search_results(html: str, page_url: str) -> Tuple[List[Dict[str, str]], str]
```  
and  
```python
get_search_url(query: str, latest: bool = True, country: str = 'us') -> str
```

## Usage Example
Construct a URL for the first results page of searching "Tesla TSLA" in Bing Search.
```python
from search_engines import bing_search

url = bing_search.get_search_url('Tesla TSLA')
```
Load the URL using a simple HTTP client or web browser and extract the page HTML.
This package does not make any restrictions on clients can be used. We'll use the `requests` library for this example.
```python
import requests

resp = requests.get(url)
html = resp.text
```
We can now extract search results from the HTML.
The returned `results` list will be a list of dictionaries with keys `url`, `title`, `preview_text`, `page_number`.
If we want to scrape multiple pages, we can load the next page using the returned `next_page_url`, and again extracting the results using `extract_search_results`.

```python
results, next_page_url = bing_search.extract_search_results(html, url)
```

## Contributions
Add new search engines! =)   