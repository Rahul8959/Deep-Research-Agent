import arxiv
from src.utils import timed

# Reused across calls; the client handles arXiv's rate limiting and retries.
_client = arxiv.Client(page_size=10, delay_seconds=3, num_retries=3)

@timed("arXiv Search")
def arxiv_search(query: str, max_results: int = 5):
    """Search arXiv and return a compact list of papers (metadata + short summary)."""
    search = arxiv.Search(query=query, max_results=max_results)

    papers = []
    for r in _client.results(search):
        papers.append(
            {
                "title": r.title,
                "authors": ", ".join(a.name for a in r.authors),
                "published": str(r.published.date()),
                "entry_id": r.entry_id,
                "summary": (r.summary or "")[:1200],
            }
        )
    return papers
