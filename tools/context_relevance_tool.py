# context_relevance_tool.py
import json
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="gpt-oss:120b-cloud")

def build_context_relevance_tool():
    """
    Tool to check if provided context is relevant to the user question.
    Accepts a single JSON string input containing both question and context.
    """
    with open("prompts/context_relevance_prompt.txt", "r", encoding="utf-8") as f:
        template_text = f.read()
    
    prompt = ChatPromptTemplate.from_template(template_text)
    chain = prompt | llm | StrOutputParser()
    
    @tool
    def context_relevance_checker(input_json: str):
        """
        input_json: '{"question": "...", "context": "..."}'
        Returns 'relevant' or 'irrelevant'.
        """
        print("Building Context Relevance Tool.................\n") 

        try:
            data = json.loads(input_json)
            question = data.get("question", "")
            context = data.get("context", "")
        except Exception:
            return json.dumps({
                "action": "ContextRelevanceChecker",
                "action_input": "invalid_input"
            })
        
        result = chain.invoke({"question": question, "context": context})
        return json.dumps({
            "action": "ContextRelevanceChecker",
            "action_input": result
        })

    context_relevance_checker.name = "ContextRelevanceChecker"
    context_relevance_checker.description = "Evaluates whether the provided context is relevant to the specific question being asked. Use this tool to verify that retrieved or user-provided information is actually useful before attempting to answer."

    return context_relevance_checker
