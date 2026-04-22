import os
from langchain_mistralai import ChatMistralAI
from deepagents import create_deep_agent

# Import tools
from src.tools.web_tools import internet_search_general, internet_search_news
from src.tools.paper_tools import arxiv_search

# Import prompts (Ensure these constants exist in your src/prompts.py)
from src.prompts import (
    MAIN_PROMPT, 
    NEWS_SUBAGENT_PROMPT, 
    ARXIV_SUBAGENT_PROMPT, 
    GENERAL_SUBAGENT_PROMPT
)

# 1. Initialize the LLM
# Using mistral-large-latest for high-reasoning orchestration
llm = ChatMistralAI(
    model="mistral-small-2603",
    mistral_api_key=os.environ.get("MISTRAL_API_KEY")
)

# 2. Define the Academic Sub-agent (arXiv)
# Specialized in technical grounding and research paper analysis
arxiv_subagent = {
    "name": "arxiv-expert",
    "description": "Use ONLY for academic papers, SOTA (State of the Art) methods, and scientific evidence.",
    "system_prompt": ARXIV_SUBAGENT_PROMPT,
    "tools": [arxiv_search],
}

# 3. Define the General Web Sub-agent (Tavily General)
# Specialized in documentation, definitions, and broad context
general_subagent = {
    "name": "web-generalist",
    "description": "Use for definitions, how-to guides, documentation, and general web background.",
    "system_prompt": GENERAL_SUBAGENT_PROMPT,
    "tools": [internet_search_general],
}

# 4. Define the News Sub-agent (Tavily News)
# Specialized in time-sensitive events and recent releases
news_subagent = {
    "name": "news-researcher",
    "description": "Use ONLY for recent updates, timelines, or anything happening 'this week' or 'recently'.",
    "system_prompt": NEWS_SUBAGENT_PROMPT,
    "tools": [internet_search_news],
}

# 5. Build the Main Orchestrator Agent
# This agent acts as the 'Router'. It doesn't have direct tools,
# but delegates to its specialized team.
DRA_agent = create_deep_agent(
    tools=[], 
    system_prompt=MAIN_PROMPT,
    subagents=[
        general_subagent, 
        arxiv_subagent, 
        news_subagent
    ],
    model=llm
)