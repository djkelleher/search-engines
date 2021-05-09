from crawler_cluster import TaskQueue
from crawler_cluster.page_loaders.loader import Loader

from search_engines import (ask_search,
                            bing_news,
                            bing_search,
                            dogpile_news,
                            dogpile_search,
                            google_news,
                            google_search,
                            yahoo_news,
                            yahoo_search)
from typing import Optional, Union, List, Dict, Any

modules = {
    'ask_search': ask_search,
    'bing_news': bing_news,
    'bing_search': bing_search,
    'dogpile_news': dogpile_news,
    'dogpile_search': dogpile_search,
    'google_news': google_news,
    'google_search': google_search,
    'yahoo_news': yahoo_news,
    'yahoo_search': yahoo_search,
}


async def search(task_data: Dict[str, Any], task_queue: TaskQueue, loader: Loader, task_executer: FunctionExecuter):
    """Start a new search task or scrape a results page for an existing search task."""
    if 'url' not in task_data:
        # this is a new search and we need to initialize tasks.
        await _start_search(task_data)
    else:
        # this is a task for scraping a results page for an existing search task.
        await _scrape_page(task_data, task_queue, loader, task_executer)


def _search_results_key(task_id: str) -> str:
    """Key to Redis List where results from search are stored."""
    return f'tmp_search_results::{task_id}'


def _get_engine_module(engine: str):
    """Check that search engine name is a valid module."""
    module = modules.get(engine)
    if module is None:
        raise ValueError(
            f"Invalid search engine: {engine}. 'engine' should be one of: {''.join(modules.keys())}")
    return module


async def _start_search(task_data: Dict[str, Any]) -> None:
    """Initialize tasks for a new search query."""
    # check if required keys are present.
    missing_keys = [k for k in (
        'query', 'engine', 'task_id') if k not in task_data]
    if missing_keys:
        raise ValueError(
            f"Argument for task_data is missing required key(s): {', '.join(missing_keys)}")
    module = _get_engine_module(task_data['engine'])
    await task_queue.put({**task_data,
                          'module': 'crawler_cluster.search_engines',
                          'function': 'search',
                          'url': module.get_search_url(task_data['query']),
                          'page_number': 1,
                          })


def _search_finished(next_results_page_url: str, task_data: Dict[str, Any]) -> bool:
    """Return True if a search is finshed."""
    if not next_results_page_url:
        # no more page to scrape. search is finished.
        return True
    if 'max_pages' not in task_data:
        # no limit on the number of pages scraped. search is not finished.
        return False
    if task_data['page_number'] < task_data['max_pages']:
        # have not reached page limit. search is not finished.
        return False
    # no condition met for declaring search not finished.
    return True


async def _scrape_page(task_data: Dict[str, Any], task_queue: TaskQueue, loader: Loader, task_executer: FunctionExecuter) -> None:
    """Scrape the results page of a search engine search."""
    # check required keys.
    missing_keys = [k for k in (
        'url', 'engine', 'task_id', 'page_number') if k not in task_data]
    if missing_keys:
        raise ValueError(
            f"Argument for task_data is missing required key(s): {', '.join(missing_keys)}")
    module = _get_engine_module(task_data['engine'])
    # load page.
    await loader.fetch(task_data['url'])
    results, next_page_url = module.extract_search_results(loader.html)
    # results is a list of Dict[str,str]
    # add results to this tasks result list.
    await task_queue.redis.lpush(_search_results_key(task_data['task_id']), pickle.dumps(results))
    # check if there is a next page that we should create a task for.
    if not _search_finished(next_page_url, task_data):
        # create task to scrape next page.
        task_data['url'] = next_page_url
        task_data['page_number'] += 1
        # queue the task.
        await task_queue.put(task_data)
    else:
        await _set_complete_search_results(task_data, task_queue, )


async def _set_complete_search_results(task_data: Dict[str, Any], task_queue: TaskQueue, task_executer: TaskExecuter) -> None:
    """Format search results into a flat list of dicts and store in results list of the task executer."""
    # pull all results from the temporary list.
    results_lists = await task_queue.redis.lrange(task_data['task_id'], 0, -1)
    # load pickled results lists and create a flat list. each list in results_lists contains data dicts from one search results page.
    results_list = []
    for l in results_list:
        results_list += pickle.loads(l)
    # add results to results cache so it can be retrieved by client.
    await task_executer.cache_task_results({
        'result': results_list,
        'task_id': task_data['task_id'],
    })
    # remove temporary list now that completed results have been moved to results list.
    await task_queue.redis.delete(_search_results_key(task_data['task_id']))
