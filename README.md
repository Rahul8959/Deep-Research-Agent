# Deep Research Agent (DeepAgents + Tavily + arXiv)

A simple research assistant built using **DeepAgents** that can:
- search the web for reliable background information (Tavily `topic="general"`)
- fetch relevant research papers (arXiv via `ArxivRetriever`)
- optionally fetch **recent updates** using a dedicated **news subagent** (Tavily `topic="news"`)

You can run it:
1) from the **console (CLI)** using `deep_research_agent.py`
2) as a **Streamlit web app** using `streamlit_app.py`

---

## Features

- **General research (Tavily - General)**  
  Finds definitions, documentation, explainers, comparisons, and background.

- **Academic grounding (arXiv)**  
  Adds relevant research papers for technical topics, with short summaries and arXiv IDs.

- **Recent updates timeline (Tavily - News subagent)**  
  For queries like “latest”, “recent”, “timeline”, “this week”, the main agent can delegate to a subagent that returns a compact timeline + sources.

- **Timing logs**  
  Prints tool timings in the console (useful for debugging and demos).

---

## Project Files

- **`deep_research_agent.py`**  
  Creates the deep research agent and exposes:
  - `DRA_agent` (agent instance)
  - `run_query(query: str)` helper
  - `extract_text_from_message(msg)` helper

- **`streamlit_app.py`**  
  A Streamlit UI that imports and runs the same agent.

---

## Setup

### 1) Create a virtual environment (recommended)

**Windows (PowerShell)**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
````

**Mac/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
Make sure your virtual environment is activated, then run:
```bash
pip install -r requirements.txt
```

### 3) Add API keys

Create a file named **`.env`** in the project root:

```env
MISTRAL_API_KEY=your_mistral_key_here
TAVILY_API_KEY=your_tavily_key_here

# Optional (LangSmith tracing)
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=
LANGSMITH_ENDPOINT=
LANGSMITH_TRACING=
```

---

## Run from Console (CLI)

```bash
python deep_research_agent.py
```

It will prompt:

```text
Enter your research query:
```

Example query:

```text
Explain RAG vs fine-tuning. Include 3–5 web sources with research papers.
```

---

## Run as Streamlit App

```bash
streamlit run streamlit_app.py
```

Then open the local URL shown in the terminal (usually `http://localhost:8501`).

The UI includes example queries you can select/copy and a textbox to run your own.

---

## Example Queries

* What is RAG in simple words?
* Explain fine-tuning in simple words.
* What is an embedding? Give a small example.
* How does semantic search work?
* What are the latest updates about AI agents this week? Give a short timeline with sources.

---

## Notes

* The **news subagent** is only used for time-sensitive questions (e.g., “latest”, “recent”, “timeline”, “this week”).
* arXiv search is mainly used for **technical/research-heavy topics** to add credible paper references.
* If a source/date cannot be verified from tool outputs, the agent is instructed to mark it as uncertain.

```
::contentReference[oaicite:0]{index=0}
```
