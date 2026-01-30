try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS
from datetime import datetime
import time
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize DuckDuckGo search
ddgs = DDGS()

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        logger.error(f"Failed after {retries} retries: {e}")
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x) + random.uniform(0, 1)
                    logger.warning(f"Error {e}, retrying in {sleep:.2f} seconds...")
                    time.sleep(sleep)
                    x += 1
        return wrapper
    return decorator

@retry_with_backoff(retries=3, backoff_in_seconds=2)
def find_places(destination: str, interests: list) -> str:
    """
    Searches for places to visit based on destination and interests.
    """
    query = f"top tourist attractions in {destination} for {', '.join(interests)} lovers"
    print(f"Searching for: {query}...")
    try:
        results = ddgs.text(query, max_results=5)
        if not results:
             return "No specific attractions found. You might want to check local listings."
        # Format results as text
        formatted_results = "\n".join([f"- {r['title']}: {r['body']}" for r in results])
        return formatted_results
    except Exception as e:
        logger.error(f"Error searching places for {destination}: {e}")
        return f"Could not retrieve attractions due to an error: {e}"

@retry_with_backoff(retries=3, backoff_in_seconds=2)
def check_weather(destination: str, date: str = None) -> str:
    """
    Checks the weather for the destination using online search.
    If date is provided, searches for historical/forecast weather for that time.
    """
    if date:
        query = f"weather in {destination} on {date}"
    else:
        # Default to current month if no date
        current_month = datetime.now().strftime("%B")
        query = f"typical weather in {destination} in {current_month}"
        
    print(f"Searching for: {query}...")
    try:
        results = ddgs.text(query, max_results=3)
        if not results:
            return "Weather information not available."
        # Format results as text
        formatted_results = "\n".join([f"- {r['body']}" for r in results])
        return formatted_results
    except Exception as e:
        logger.error(f"Error checking weather for {destination}: {e}")
        return "Weather information unavailable due to network error."

@retry_with_backoff(retries=2, backoff_in_seconds=1)
def validate_place(place_name: str, destination: str) -> dict:
    """
    Validates if a specific place exists in the destination.
    Returns a dict with 'exists' (bool) and 'info' (str) keys.
    """
    query = f"{place_name} in {destination} opening hours contact"
    try:
        results = ddgs.text(query, max_results=2)
        if results and len(results) > 0:
            info = results[0]['body'][:200] if results else ""
            return {
                "exists": True,
                "info": info
            }
        else:
            return {
                "exists": False,
                "info": "Could not verify this location."
            }
    except Exception as e:
        logger.warning(f"Error validating place {place_name}: {e}")
        return {
            "exists": None,  # Unknown status
            "info": "Validation unavailable."
        }
