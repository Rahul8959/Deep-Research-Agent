import os
from tavily import TavilyClient
from src.utils import timed

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

@timed("Tavily General Search")
def internet_search_general(query: str, max_results: int = 5):
    """Search the web for background/general information using Tavily (topic=general)."""
    return tavily_client.search(query, max_results=max_results, topic="general")

@timed("Tavily News Search")
def internet_search_news(query: str, max_results: int = 8, days: int = 7):
    """Search the web for recent/news information using Tavily (topic=news) for the last N days."""
    return tavily_client.search(query, max_results=max_results, topic="news", days=days)