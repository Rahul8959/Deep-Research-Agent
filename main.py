import time
import sys
from dotenv import load_dotenv

# MUST be loaded before src imports
load_dotenv()

from src.agent import DRA_agent
from src.utils import extract_text_from_message

def run_query(query: str) -> str:
    t0 = time.perf_counter()
    print(f"\n[QUERY] {query}")
    print("Thinking... (Delegating to sub-agents)\n")
    
    try:
        # Invoke the orchestrator
        result = DRA_agent.invoke({"messages": [{"role": "user", "content": query}]})
        
        dt = time.perf_counter() - t0
        print(f"\n[TOTAL] Completed in {dt:.2f}s\n")
        
        return extract_text_from_message(result["messages"][-1])

    except Exception as e:
        # Graceful failure for API timeouts or rate limits
        dt = time.perf_counter() - t0
        print(f"\n[ERROR] The agent encountered an issue after {dt:.2f}s.")
        print(f"Details: {str(e)}")
        return "Research aborted due to an error."

if __name__ == "__main__":
    print("Welcome to the Deep Research CLI.")
    print("Type 'exit' or 'quit' to close.")
    print("-" * 30)
    
    while True:
        q = input("\nEnter your research query: ").strip()
        
        if q.lower() in ['exit', 'quit']:
            print("Exiting...")
            sys.exit(0)
            
        if not q:
            continue
            
        print(run_query(q))
        print("-" * 50)