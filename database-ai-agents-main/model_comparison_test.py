"""
Model Comparison Test
Tests gpt-3.5-turbo vs gpt-4.1-mini vs claude-haiku-4.5 against ground truth
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import time

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")

# Load data
df = pd.read_csv("./data/salaries_2023.csv").fillna(value=0)

# Prompt setup
CSV_PROMPT_PREFIX = """
First set the pandas display options to show all the columns,
get the column names, then answer the question.
"""

CSV_PROMPT_SUFFIX = """
- **ALWAYS** before giving the Final Answer, try another method.
Then reflect on the answers of the two methods you did and ask yourself
if it answers correctly the original question.
If you are not sure, try another method.
FORMAT 4 FIGURES OR MORE WITH COMMAS.
- If the methods tried do not give the same result,reflect and
try again until you have two methods that have the same result.
- If you still cannot arrive to a consistent result, say that
you are not sure of the answer.
- If you are sure of the correct answer, create a beautiful
and thorough response using Markdown.
- **DO NOT MAKE UP AN ANSWER OR USE PRIOR KNOWLEDGE,
ONLY USE THE RESULTS OF THE CALCULATIONS YOU HAVE DONE**.
- **ALWAYS**, as part of your "Final Answer", explain how you got
to the answer on a section that starts with: "\\n\\nExplanation:\\n".
In the explanation, mention the column names that you used to get
to the final answer.
"""

QUESTION = "Which grade has the highest average base salary, and compare the average female pay vs male pay?"

# Models: (model_name, display_name, provider, agent_type)
models = [
    ("gpt-3.5-turbo", "GPT-3.5-Turbo", "openai", "openai-tools"),
    ("gpt-4.1-mini-2025-04-14", "GPT-4.1-mini", "openai", "openai-tools"),
    ("claude-haiku-4-5-20251001", "Claude Haiku 4.5", "anthropic", "tool-calling"),
]

print("=" * 100)
print("MODEL COMPARISON TEST - Accuracy Verification")
print("=" * 100)
print("\n📊 Ground Truth (Direct Pandas):")
print("  - Highest grade overall: EX0 ($292,000.00) - only has 1 male employee")
print("  - Highest grade with both genders: EX1 ($225,958.33)")
print("    • Female in EX1: $226,000.00")
print("    • Male in EX1: $225,937.50")
print("  - Overall gender pay comparison:")
print("    • Female average (all grades): $87,497.50")
print("    • Male average (all grades): $92,382.93")
print("    • Gap: $4,885.43 (Male higher)")
print("\n" + "=" * 100)

for model_name, display_name, provider, agent_type in models:
    print(f"\n\n🤖 Testing {display_name} ({model_name})")
    print(f"   Provider: {provider.upper()} | Agent Type: {agent_type}")
    print("-" * 100)

    # Create model based on provider
    if provider == "anthropic":
        model = ChatAnthropic(api_key=anthropic_key, model=model_name, temperature=0)
    else:
        model = ChatOpenAI(api_key=openai_key, model=model_name, temperature=0)

    agent = create_pandas_dataframe_agent(
        llm=model,
        df=df,
        agent_type=agent_type,  # Use appropriate agent type for each model
        verbose=False,  # Suppress intermediate steps for cleaner output
        allow_dangerous_code=True,
        max_iterations=30,
    )

    start_time = time.time()
    try:
        res = agent.invoke(CSV_PROMPT_PREFIX + QUESTION + CSV_PROMPT_SUFFIX)
        elapsed = time.time() - start_time

        print(f"\n⏱️  Response time: {elapsed:.2f}s")
        print(f"\n📝 Answer:")
        print("-" * 100)
        # Handle both string and list outputs
        output = res['output'] if isinstance(res['output'], str) else res['output'][0].get('text', str(res['output']))
        print(output)
        print("-" * 100)

    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ Error after {elapsed:.2f}s: {str(e)}")

print("\n\n" + "=" * 100)
print("COMPARISON COMPLETE")
print("=" * 100)
print("\n💡 How to evaluate accuracy:")
print("  1. Check if the model identified EX0 as highest grade ($292,000)")
print("  2. Check if overall gender comparison is accurate:")
print("     - Female average: $87,497.50")
print("     - Male average: $92,382.93")
print("     - Gap: $4,885.43 (Male higher)")
print("  3. Check if it tried two methods and verified results")
print("  4. Check if final answer matches intermediate calculations")
print("\n⚠️  Note: Claude may have correct calculations but wrong final summary")
print("=" * 100)
