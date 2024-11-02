#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
Obtain the HTML content of a particular URL and return it.
"""
import redis
import requests

# Connect to the Redis server
r = redis.Redis()

def get_page(url: str) -> str:
    """
    Track how many times a particular URL was accessed
    in the key "count:{url}", and cache the result with an
    expiration time of 10 seconds.
    """
    # Increment the access count
    r.incr(f"count:{url}")
    
    # Check if the content is already cached
    cached_content = r.get(f"cached:{url}")
    if cached_content:
        print("Cache hit!")
        return cached_content.decode("utf-8")
    
    # If not cached, fetch the content and cache it
    print("Cache miss! Fetching from the web...")
    resp = requests.get(url)
    
    # Cache the content with a 10-second expiration
    r.setex(f"cached:{url}", 10, resp.text)
    
    return resp.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
