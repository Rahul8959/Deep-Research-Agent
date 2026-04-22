# Deep Research Agent

A multi-agent research assistant that searches the web, arXiv, and recent news, then synthesizes a clear, cited answer.

**Live demo:** https://deep-dive-research.streamlit.app/

Built with [DeepAgents](https://github.com/langchain-ai/deepagents) on top of LangChain/LangGraph, powered by [Mistral AI](https://mistral.ai/) for reasoning and orchestration, [Tavily](https://tavily.com/) for web search, and [arXiv](https://arxiv.org/) for academic papers.

---

## Architecture

A lead **orchestrator** agent analyzes each user query and delegates to three specialized sub-agents:

| Sub-agent | Role | Tool |
|---|---|---|
| `web-generalist` | Definitions, documentation, tutorials, general background | Tavily (topic=general) |
| `arxiv-expert` | Academic papers, SOTA methods, scientific evidence | arXiv |
| `news-researcher` | Recent updates, timelines, releases, announcements | Tavily (topic=news) |

The orchestrator then merges findings into a single structured report with inline source URLs / arXiv IDs.

---

## Features

- **Multi-source research** — web + academic papers + recent news, from a single query
- **Cited answers** — source URLs and arXiv IDs attached to every claim
- **Streaming UI** — answers render live as the agent works
- **Light / dark mode** — toggle in the sidebar
- **CLI mode** — run from the terminal without the UI

---

## Project structure

```
Deep-Research-Agent/
├── main.py                  # CLI entry point
├── streamlit_app.py         # Streamlit UI entry point
├── requirements.txt
├── src/
│   ├── agent.py             # Builds the orchestrator + sub-agents
│   ├── prompts.py           # System prompts for each agent
│   ├── utils.py             # Timing decorator, text helpers
│   └── tools/
│       ├── web_tools.py     # Tavily general + news search
│       └── paper_tools.py   # arXiv retrieval
├── .streamlit/
│   └── config.toml          # Streamlit theme config
├── .env.example             # Template for API keys
└── README.md
```

---

## Setup

### 1. Clone and create a virtual environment

```bash
git clone https://github.com/Rahul8959/Deep-Research-Agent.git
cd Deep-Research-Agent
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your API keys

Copy the template and fill in your real keys:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
MISTRAL_API_KEY=your_mistral_key_here
TAVILY_API_KEY=your_tavily_key_here
```

- Mistral API key — https://console.mistral.ai/api-keys (free tier works)
- Tavily API key — https://tavily.com/ (free tier: 1,000 searches/month)

---

## Usage

### Run the Streamlit UI (recommended)

```bash
streamlit run streamlit_app.py
```

Opens at `http://localhost:8501`.

### Run the CLI

```bash
python main.py
```

Then type queries at the prompt. `exit` or `quit` to close.

---

## Example queries

- *"Compare RAG vs. fine-tuning for enterprise search."*
- *"What is the state of the art in LLM-based agents?"*
- *"Summarize recent advances in diffusion models on arXiv."*
- *"What are the latest updates about AI agents this week? Give a short timeline with sources."*

Time-sensitive queries (containing words like *latest*, *recent*, *timeline*, *this week*) automatically trigger the news sub-agent.

---

## Model

Uses `mistral-small-2603` by default — chosen for its generous free-tier limits (400 RPM, 1.5M TPM) which comfortably handle the multi-agent fan-out. The model ID is set in `src/agent.py` and can be swapped to any other Mistral model.

---

## Deployment

The live demo at [deep-dive-research.streamlit.app](https://deep-dive-research.streamlit.app/) is deployed on [Streamlit Community Cloud](https://share.streamlit.io). API keys are managed through Streamlit Cloud's secrets manager, not committed to the repo.

---

## License

MIT
