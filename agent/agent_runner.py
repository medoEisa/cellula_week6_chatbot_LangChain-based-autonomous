import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_ollama import ChatOllama
from langchain_classic.agents import initialize_agent, AgentType
from tools.context_judge import build_context_presence_tool
from tools.web_search_tool import build_web_search_tool
from tools.context_relevance_tool import build_context_relevance_tool
from tools.context_splitter import build_context_splitter_tool


# Build tools
context_judge_tool = build_context_presence_tool()
web_search_tool = build_web_search_tool(max_results=3)
context_relevance_checker_tool = build_context_relevance_tool() 
context_splitter_tool = build_context_splitter_tool()



tools = [context_judge_tool, web_search_tool,context_relevance_checker_tool,context_splitter_tool]

# Initialize REACT Agent
agent = initialize_agent(
    tools,
    llm=ChatOllama(model="gpt-oss:120b-cloud"),  
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True
)

if __name__ == "__main__":
    test_query = "what is classcorer paper. after answering, tell what function did you use to get the answer and handle if context was missing or not , context relevance check and  context splitting and please give me the name of functions used"

    print("=== Running autonomous REACT agent ===\n")
    result = agent.run({"input":test_query, "chat_history":[]})

    # The output might include reasoning and final result
    print("\n=== Agent Final Output ===")
    print(result)