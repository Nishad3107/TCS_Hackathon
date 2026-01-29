from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()

def find_places(destination: str, interests: list) -> str:
    """
    Searches for places to visit based on destination and interests.
    """
    query = f"top tourist attractions in {destination} for {', '.join(interests)} lovers"
    print(f"Searching for: {query}...")
    try:
        results = search_tool.invoke(query)
        return results
    except Exception as e:
        return f"Error searching places: {e}"

def check_weather(destination: str, date: str) -> str:
    """
    Mock weather tool (Real weather APIs usually require keys/paid access).
    """
    return f"Typical weather in {destination} during this time is mild and pleasant."
