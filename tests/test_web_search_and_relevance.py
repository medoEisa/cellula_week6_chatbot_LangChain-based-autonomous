import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.web_search_tool import build_web_search_tool
from tools.context_relevance_tool import build_context_relevance_tool
from langchain_ollama import ChatOllama  # same LLM for all tools

llm = ChatOllama(model="gpt-oss:120b-cloud")

# Build tools
web_search_tool = build_web_search_tool(top_n=2)  # 2 top results to keep it fast
relevance_tool = build_context_relevance_tool(llm)

# Test cases: (question, search_query)
test_cases = [
    ("What are the latest breakthroughs in quantum computing 2024?", "quantum computing breakthroughs 2024"),
    ("Who won the FIFA World Cup in 2022?", "FIFA World Cup 2022 winner"),
    ("Explain AI ethics concerns in large language models.", "AI ethics in LLMs"),
    ("What are the health benefits of eating broccoli?", "broccoli nutrition benefits"),
    ("What is the latest Mars rover mission update?", "Mars rover latest news"),
    ("Tell me about the top movies of 2023.", "top movies released 2023"),
    ("Who is the CEO of Tesla in 2025?", "Tesla CEO 2025"),
    ("Explain climate change impacts on polar bears.", "climate change effect polar bears"),
    ("What is the fastest animal in the world?", "fastest animal on Earth"),
    ("Describe the key features of the iPhone 15.", "iPhone 15 features 2025")
]

# Run tests
for i, (question, query) in enumerate(test_cases, start=1):
    print(f"\n--- Test Case {i} ---")
    # Step 1: Run web search tool
    web_result_json = web_search_tool.invoke(query)
    
    # Extract aggregated content for relevance checking
    import json
    web_result = json.loads(web_result_json)
    context_text = web_result.get("action_input", "")
    
    # Step 2: Test Context Relevance Checker
    relevance_result_json = relevance_tool.invoke({
        "question": question,
        "context": context_text
        })
    relevance_result = json.loads(relevance_result_json)
    
    print("Question:", question)
    print("Web Search Query:", query)
    print("Web Search Context Snippet (first 300 chars):", context_text[:300], "...")
    print("Context Relevance Result:", relevance_result["action_input"])
