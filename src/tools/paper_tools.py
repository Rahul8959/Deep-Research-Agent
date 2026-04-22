from langchain_community.retrievers import ArxivRetriever
from src.utils import timed

@timed("arXiv Search")
def arxiv_search(query: str, max_results: int = 5, get_full_documents: bool = False):
    """Search arXiv and return a compact list of papers (metadata + short summary)."""
    retriever = ArxivRetriever(
        load_max_docs=max_results,
        get_full_documents=get_full_documents,
        load_all_available_meta=False,
        continue_on_failure=True,
    )
    docs = retriever.invoke(query)

    papers = []
    for d in docs:
        md = d.metadata or {}
        papers.append(
            {
                "title": md.get("Title"),
                "authors": md.get("Authors"),
                "published": str(md.get("Published")),
                "entry_id": md.get("Entry ID"),
                "summary": (d.page_content or "")[:1200],
            }
        )
    return papers