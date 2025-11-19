from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

import json
llm = ChatOllama(model="gpt-oss:120b-cloud")

def build_context_presence_tool():
    """
    Checks if context is present in user input
    Flow: First tool invoked by agent for every query.  If 'no', calls web_search_tool.
    """
    with open("prompts/context_judge_prompt.txt", "r", encoding="utf-8") as f:
        template_text = f.read()

    prompt = ChatPromptTemplate.from_template(template_text)

    # Build the chain
    chain = prompt | llm | StrOutputParser()
    
    @tool
    def context_presence_judge(query: str):
        """
        Checks if context is present in user input
        """
        print("Building Context Presence Judge Tool.......................")

        result = chain.invoke({"input": query})
        return json.dumps({
        "action": "ContextPresenceJudge",
        "action_input": result
            })

    context_presence_judge.name = "ContextPresenceJudge"
    context_presence_judge.description = "Checks if context is present in user input. context_provided context_missing Only if 'context_missing', call web_search_tool."

    return context_presence_judge



# if __name__ == "__main__":
#     judge_tool = build_context_presence_tool(llm)
#     question = "hello how are you?"
#     result = judge_tool.invoke(question)
#     print(result)