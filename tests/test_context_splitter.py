import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.context_splitter import build_context_splitter_tool  # make sure your splitter instance is imported correctly
splitter_tool = build_context_splitter_tool()
# 20 test cases
test_cases = [
    # 1
    {
        "input": "I read about quantum computing in 2024. What are the key breakthroughs?",
        "expected": {
            "background_context": "I read about quantum computing in 2024.",
            "actual_question": "What are the key breakthroughs?"
        }
    },
    # 2
    {
        "input": "Explain Newton's laws of motion.",
        "expected": {
            "background_context": "",
            "actual_question": "Explain Newton's laws of motion."
        }
    },
    # 3
    {
        "input": "After studying the history of AI from the 1950s to 2023, including expert opinions on machine learning algorithms, I want to know what AI trends will dominate 2025.",
        "expected": {
            "background_context": "After studying the history of AI from the 1950s to 2023, including expert opinions on machine learning algorithms.",
            "actual_question": "I want to know what AI trends will dominate 2025."
        }
    },
    # 4
    {
        "input": "I recently saw an article about climate change impacts. It discussed rising sea levels and extreme weather. Can you summarize the main points?",
        "expected": {
            "background_context": "I recently saw an article about climate change impacts. It discussed rising sea levels and extreme weather.",
            "actual_question": "Can you summarize the main points?"
        }
    },
    # 5
    {
        "input": "Considering the recent advances in CRISPR gene editing, how might this affect personalized medicine?",
        "expected": {
            "background_context": "Considering the recent advances in CRISPR gene editing.",
            "actual_question": "How might this affect personalized medicine?"
        }
    },
    # 6
    {
        "input": "I am reading about renewable energy. How efficient is solar power? How does wind compare?",
        "expected": {
            "background_context": "I am reading about renewable energy.",
            "actual_question": "How efficient is solar power? How does wind compare?"
        }
    },
    # 7
    {
        "input": "I have been studying string theory and the multiverse theory extensively.",
        "expected": {
            "background_context": "I have been studying string theory and the multiverse theory extensively.",
            "actual_question": ""
        }
    },
    # 8
    {
        "input": "What is the difference between supervised and unsupervised learning?",
        "expected": {
            "background_context": "",
            "actual_question": "What is the difference between supervised and unsupervised learning?"
        }
    },
    # 9
    {
        "input": "The stock market has been volatile in 2024. What are the predictions for 2025?",
        "expected": {
            "background_context": "The stock market has been volatile in 2024.",
            "actual_question": "What are the predictions for 2025?"
        }
    },
    # 10
    {
        "input": "As Einstein once said, 'Imagination is more important than knowledge.' How does this apply to modern AI research?",
        "expected": {
            "background_context": "As Einstein once said, 'Imagination is more important than knowledge.'",
            "actual_question": "How does this apply to modern AI research?"
        }
    },
    # 11
    {
        "input": "Considering the formula E=mc^2, what are its implications for nuclear energy?",
        "expected": {
            "background_context": "Considering the formula E=mc^2.",
            "actual_question": "What are its implications for nuclear energy?"
        }
    },
    # 12
    {
        "input": "I just read a news report on fusion energy.\n\nCan you summarize the key takeaways?",
        "expected": {
            "background_context": "I just read a news report on fusion energy.",
            "actual_question": "Can you summarize the key takeaways?"
        }
    },
    # 13
    {
        "input": "In the 2024 IPCC report (Intergovernmental Panel on Climate Change), they emphasized CO2 reduction. What are the most effective strategies?",
        "expected": {
            "background_context": "In the 2024 IPCC report (Intergovernmental Panel on Climate Change), they emphasized CO2 reduction.",
            "actual_question": "What are the most effective strategies?"
        }
    },
    # 14
    {
        "input": "Paragraph 1: Deep learning has revolutionized image recognition.\nParagraph 2: CNNs and transformers dominate the field.\nQuestion: How do transformers outperform CNNs in large datasets?",
        "expected": {
            "background_context": "Paragraph 1: Deep learning has revolutionized image recognition.\nParagraph 2: CNNs and transformers dominate the field.",
            "actual_question": "How do transformers outperform CNNs in large datasets?"
        }
    },
    # 15
    {
        "input": "I read about quantum computing and classical supercomputers. Which tasks are better suited for quantum computing?",
        "expected": {
            "background_context": "I read about quantum computing and classical supercomputers.",
            "actual_question": "Which tasks are better suited for quantum computing?"
        }
    },
    # 16
    {
        "input": "I am preparing a lecture on AI. Please summarize key points about reinforcement learning.",
        "expected": {
            "background_context": "I am preparing a lecture on AI.",
            "actual_question": "Please summarize key points about reinforcement learning."
        }
    },
    # 17
    {
        "input": "Explain black holes.",
        "expected": {
            "background_context": "",
            "actual_question": "Explain black holes."
        }
    },
    # 18
    {
        "input": "In 2024, MIT demonstrated superconductivity in twisted trilayer graphene at 30 K. How does this impact quantum computer design?",
        "expected": {
            "background_context": "In 2024, MIT demonstrated superconductivity in twisted trilayer graphene at 30 K.",
            "actual_question": "How does this impact quantum computer design?"
        }
    },
    # 19
    {
        "input": "I read <b>an article on AI ethics</b>. What are the main concerns for 2025?",
        "expected": {
            "background_context": "I read <b>an article on AI ethics</b>.",
            "actual_question": "What are the main concerns for 2025?"
        }
    },
    # 20
    {
        "input": "After reading about fusion energy advancements can you explain the key engineering challenges?",
        "expected": {
            "background_context": "After reading about fusion energy advancements",
            "actual_question": "Can you explain the key engineering challenges?"
        }
    },
]

# -------------------------------
# RUN TESTS
# -------------------------------
for idx, case in enumerate(test_cases, start=1):
    input_text = case["input"]
    expected = case["expected"]

    try:
        output = splitter_tool.invoke(input_text)
        if isinstance(output, str):
            output_json = json.loads(output)
        else:
            output_json = output

        # Extract action_input if present
        if "action_input" in output_json:
            output_json = output_json["action_input"]

        if output_json == expected:
            print(f"✅ Test {idx} passed.")
        else:
            print(f"❌ Test {idx} failed.")
            print(f"Input: {input_text}")
            print(f"Expected: {json.dumps(expected, indent=2)}")
            print(f"Got: {json.dumps(output_json, indent=2)}")

    except Exception as e:
        print(f"⚠️ Test {idx} raised an exception: {str(e)}")
