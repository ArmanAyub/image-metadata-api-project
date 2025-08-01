# Image Analysis & Metadata API

This project is a high-performance web API built with Python and FastAPI that extracts image metadata from provided URLs. It features a custom-built Least Recently Used (LRU) cache to demonstrate effective memory management and dramatically boost performance for repeated requests.

## Core Features

- **REST API Endpoint:** Simple `/analyze` endpoint for image processing.
- **Image Metadata Extraction:** Utilizes Pillow to extract format, size, and color mode.
- **Custom LRU Cache:** In-memory cache (built from scratch) to avoid redundant processing and showcase memory/data structure skills.

## Performance Demonstration

Caching dramatically improves performance for repeated image analyses. The first request ("cache miss") processes the image; subsequent requests ("cache hit") serve results nearly instantly from memory.

| Request Type         | Response Time     | Memory Usage (Approx.) | Notes                         |
|:---------------------|:-----------------|:-----------------------|:------------------------------|
| **Cache MISS**       | ~2.1 seconds     | ~15 MiB                | Full analysis runs            |
| **Cache HIT**        | ~0.01 seconds    | ~0.1 MiB               | Served instantly from cache   |

## Tech Stack

- **Python 3.10+**
- **FastAPI** – High-performance API framework.
- **Uvicorn** – ASGI server.
- **Pillow** – Image processing.
- **Requests** – For fetching remote images.
- **memory-profiler** – Used for analyzing cache efficiency.

## Setup and Installation

**Clone the repository:**
"""
git clone https://github.com/ArmanAyub/image-metadata-api-project.git
cd image-api-project
"""

text

**Create and activate a virtual environment:**
- _Using `venv` (recommended):_
    ```
    python -m venv venv
    source venv/bin/activate      # On Windows: venv\Scripts\activate
    ```
- _Using conda:_
    ```
    conda create --name image_api_env python=3.10
    conda activate image_api_env
    ```

**Install dependencies:**
 ```
pip install -r requirements.txt
 ```


**Run the application:**
 ```
uvicorn main:app --reload
 ```

The API will now be running at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## API Usage

You can interact with the API using any HTTP client (e.g., `curl`, Postman).

### 1. Analyze Image

- **Endpoint:** `POST /analyze`
- **Description:** Accepts an image URL, analyzes it, and returns metadata. The first request is slow (miss), subsequent identical requests are fast (hit, via cache).

#### Example: Real Usage (Miss and Hit)

**First request (Cache MISS):**
 ```
curl -X POST -H "Content-Type: application/json"
-d "{"image_url": "https://upload.wikimedia.org/wikipedia/commons/9/97/The_Earth_seen_from_Apollo_17.jpg\"}"
http://127.0.0.1:8000/analyze
 ```

text
_Response:_
{
"status": "success",
"result": {
"format": "JPEG",
"size": "800x802",
"mode": "RGB"
}
}

text
*(First call may take ~2 seconds as analysis runs.)*

**Second request (Cache HIT):**
 ```
curl -X POST -H "Content-Type: application/json"
-d "{"image_url": "https://upload.wikimedia.org/wikipedia/commons/9/97/The_Earth_seen_from_Apollo_17.jpg\"}"
http://127.0.0.1:8000/analyze
 ```

text
_Response:_
{
"status": "success (from cache)",
"result": {
"format": "JPEG",
"size": "800x802",
"mode": "RGB"
}
}

text
*(Second call is almost instant as the result is cached.)*

### 2. Status Check

- **Endpoint:** `GET /status`
- **Description:** Health check for the API.

**Example:**
 ```
curl http://127.0.0.1:8000/status
 ```

text
_Response:_
{
"status": "ok"
}

text

### 3. View Cache History

- **Endpoint:** `GET /history`
- **Description:** Shows all image URLs currently stored in the LRU cache.

**Example:**
 ```
curl http://127.0.0.1:8000/history
 ```

text
_Response:_
{
"cached_items": [
"https://upload.wikimedia.org/wikipedia/commons/9/97/The_Earth_seen_from_Apollo_17.jpg"
],
"count": 1
}

text

## Error Handling & Edge Case Notes

- **Invalid URL or unreachable image:**  
    ```
    {
      "status": "error",
      "message": "Failed to retrieve or process the image. Please check the URL."
    }
    ```
- **Corrupted or unsupported image file:**  
    ```
    {
      "status": "error",
      "message": "Unsupported image format or corrupted file."
    }
    ```
- **Cache Behavior:** Only successful analyses are stored. The cache evicts the least recently used entries automatically when full.

## Code Structure & Comments

The project emphasizes clarity and maintainability:
- Key components (like the custom LRU cache) are thoroughly commented for future contributors and reviewers.
- See source code for inline explanations, especially for cache logic and API routes.

## Contributing & Feedback

- Issues, suggestions, or pull requests are welcome!
- Please add tests for new features and thoroughly document your changes.


