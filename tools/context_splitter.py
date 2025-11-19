# tools/context_splitter.py
import json
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

# Load your LLM
llm = ChatOllama(model="gpt-oss:120b-cloud")

def build_context_splitter_tool():
    """
    Tool 4: Context Splitter
    Purpose: Separate background context from the actual question
    """

    # Load prompt from file
    with open("prompts/context_splitter_prompt.txt", "r", encoding="utf-8") as f:
        template_text = f.read()

    # Create prompt template
    prompt = ChatPromptTemplate.from_template(template_text)

    # Build chain
    chain = prompt | llm | StrOutputParser()

    @tool
    def context_splitter(user_input: str):
        """
        Splits input into background context and actual question.
        Returns JSON with keys: background_context, actual_question
        """
        print("---------------------------ContextSplitter received input :", user_input)
        result = chain.invoke({"input": user_input})
        try:
            # Ensure valid JSON output
            parsed = json.loads(result)
        except json.JSONDecodeError:
            parsed = {"background_context": "", "actual_question": ""}
        
        return json.dumps({
            "action": "ContextSplitter",
            "action_input": parsed
        })

    context_splitter.name = "ContextSplitter"
    context_splitter.description = "Separates the user input into two parts: background context and the actual question. Use this tool whenever the input contains extra information or explanation, so the agent can reason over the context and answer the question accurately."

    return context_splitter


# -----------------------------------
# Optional standalone test
# -----------------------------------
if __name__ == "__main__":
    splitter_tool = build_context_splitter_tool()
    test_input = (
        "I recently read about quantum computing breakthroughs in 2024. Can you explain the key advancements?"
    )
    print(splitter_tool.invoke(test_input))
