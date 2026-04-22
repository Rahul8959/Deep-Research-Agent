import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

load_dotenv()

os.environ.get("MISTRAL_API_KEY")
os.environ.get("TAVILY_API_KEY")
os.environ.get("LANGSMITH_API_KEY")
os.environ.get("LANGSMITH_PROJECT")
os.environ.get("LANGSMITH_ENDPOINT")
os.environ.get("LANGSMITH_TRACING")

# Magistral = Mistral's open-weight reasoning model line; the `-small-latest`
# alias is available on the free La Plateforme tier (rate-limited).
llm = ChatMistralAI(
    model="magistral-small-latest",
)
