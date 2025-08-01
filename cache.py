# cache.py

from collections import OrderedDict

class LRUCache:
    """
    A custom Least Recently Used (LRU) cache.
    It stores a limited number of items and discards the least recently used
    item when its capacity is exceeded.
    """
    def __init__(self, maxsize: int = 128):
        # We use an OrderedDict because it remembers insertion order,
        # which is perfect for knowing which item is the "oldest".
        self.cache = OrderedDict()
        self.maxsize = maxsize
        print(f"Custom cache initialized with maxsize = {self.maxsize}")

    def get(self, key: str):
        """Retrieves an item from the cache and marks it as recently used."""
        if key not in self.cache:
            return None
        
        # KEY LEARNING: move_to_end() marks an item as "most recently used".
        print(f"Cache HIT for key: {key}")
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: str, value):
        """Adds or updates an item in the cache."""
        print(f"Cache MISS. Storing key: {key}")
        self.cache[key] = value
        self.cache.move_to_end(key) # Mark it as the newest item

        # KEY LEARNING: This is where we actively manage memory.
        if len(self.cache) > self.maxsize:
            # popitem(last=False) removes the *first* item inserted,
            # which is our "least recently used".
            oldest = self.cache.popitem(last=False)
            print(f"Cache full. Evicting oldest item: {oldest[0]}")