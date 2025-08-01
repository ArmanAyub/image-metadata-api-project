# main.py (Updated)

import time
import requests
import io
from fastapi import FastAPI
from pydantic import BaseModel
from PIL import Image

# NEW: Import our cache
from cache import LRUCache

from memory_profiler import profile

app = FastAPI()

# NEW: Create a single, global instance of our cache.
cache = LRUCache(maxsize=10)

class ImageRequest(BaseModel):
    image_url: str


@profile
def analyze_image(image_url: str) -> dict:
    # ... (this function remains exactly the same) ...
    print(f"Analyzing {image_url}... this will be slow.")
    response = requests.get(image_url)
    response.raise_for_status()
    image_bytes = io.BytesIO(response.content)
    img = Image.open(image_bytes)
    time.sleep(2)
    analysis_result = {
        "format": img.format,
        "size": f"{img.width}x{img.height}",
        "mode": img.mode,
    }
    img.close()
    return analysis_result


@app.post("/analyze")
def analyze_endpoint(request: ImageRequest):
    """API endpoint that now uses a cache."""
    image_url = request.image_url

    # --- KEY LOGIC CHANGE ---
    # 1. Check the cache first
    cached_result = cache.get(image_url)
    if cached_result:
        # If we found it, return it immediately
        return {"status": "success (from cache)", "result": cached_result}

    # 2. If not in cache, run the slow function
    result = analyze_image(image_url)

    # 3. Store the new result in the cache for next time
    cache.put(image_url, result)

    return {"status": "success (newly analyzed)", "result": result}


@app.get("/status")
def get_status():
    """A simple endpoint to check if the API is running."""
    return {"status": "ok"}


@app.get("/history")
def get_history():
    """Returns a list of all image URLs currently in the cache."""
    cached_items = list(cache.cache.keys())
    return {"cached_items": cached_items, "count": len(cached_items)}