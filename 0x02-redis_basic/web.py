#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
obtain the HTML content of a particular URL and returns it
"""
import redis
import requests
from typing import Callable

# Connect to the Redis server
cache = redis.Redis(host='localhost', port=6379, db=0)

def cache_with_count_and_expiration(expiration: int):
    """A decorator for caching HTML content and tracking URL access counts."""
    def decorator(func: Callable):
        def wrapper(url: str) -> str:
            # Construct the cache and count keys
            cache_key = f"cache:{url}"
            count_key = f"count:{url}"
            
            # Increment the access count
            cache.incr(count_key)
            
            # Check if the HTML content is already cached
            cached_content = cache.get(cache_key)
            if cached_content:
                print("Cache hit!")
                return cached_content.decode("utf-8")
            
            # If not cached, fetch the content and store it in Redis
            print("Cache miss! Fetching from the web...")
            html_content = func(url)
            cache.setex(cache_key, expiration, html_content)
            return html_content
        return wrapper
    return decorator

@cache_with_count_and_expiration(expiration=10)
def get_page(url: str) -> str:
    """Fetches the HTML content of a URL and caches it."""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
