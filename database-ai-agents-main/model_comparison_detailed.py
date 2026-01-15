"""
Detailed Model Comparison Test
Tests models with multiple agent types to understand parameter impact
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

# Extended test matrix: (model_name, display_name, provider, agent_type, temperature)
test_configs = [
    # OpenAI models with different agent types
    ("gpt-4.1-mini-2025-04-14", "GPT-4.1-mini [openai-tools]", "openai", "openai-tools", 0),
    ("gpt-4.1-mini-2025-04-14", "GPT-4.1-mini [zero-shot-react]", "openai", "zero-shot-react-description", 0),

    # Claude with tool-calling (only compatible option)
    ("claude-haiku-4-5-20251001", "Claude Haiku 4.5 [tool-calling]", "anthropic", "tool-calling", 0),

    # GPT-3.5 for comparison
    ("gpt-3.5-turbo", "GPT-3.5-Turbo [openai-tools]", "openai", "openai-tools", 0),
]

print("=" * 100)
print("DETAILED MODEL COMPARISON TEST - Parameter Impact Analysis")
print("=" * 100)
print("\n📊 Ground Truth (Direct Pandas):")
print("  - Highest grade: EX0 ($292,000.00)")
print("  - Female average (all): $87,497.50")
print("  - Male average (all): $92,382.93")
print("  - Gap: $4,885.43 (Male higher)")
print("\n" + "=" * 100)

results_summary = []

for model_name, display_name, provider, agent_type, temperature in test_configs:
    print(f"\n\n🤖 Testing {display_name}")
    print(f"   Model: {model_name}")
    print(f"   Provider: {provider.upper()} | Agent Type: {agent_type} | Temperature: {temperature}")
    print("-" * 100)

    # Create model based on provider
    if provider == "anthropic":
        model = ChatAnthropic(api_key=anthropic_key, model=model_name, temperature=temperature)
    else:
        model = ChatOpenAI(api_key=openai_key, model=model_name, temperature=temperature)

    agent = create_pandas_dataframe_agent(
        llm=model,
        df=df,
        agent_type=agent_type,
        verbose=False,
        allow_dangerous_code=True,
        max_iterations=30,
    )

    start_time = time.time()
    try:
        res = agent.invoke(CSV_PROMPT_PREFIX + QUESTION + CSV_PROMPT_SUFFIX)
        elapsed = time.time() - start_time

        # Handle both string and list outputs
        output = res['output'] if isinstance(res['output'], str) else res['output'][0].get('text', str(res['output']))

        print(f"\n⏱️  Response time: {elapsed:.2f}s")
        print(f"\n📝 Answer (first 500 chars):")
        print("-" * 100)
        print(output[:500] + ("..." if len(output) > 500 else ""))
        print("-" * 100)

        # Check for accuracy markers
        has_ex0 = "EX0" in output or "Ex0" in output or "ex0" in output
        has_292000 = "292,000" in output or "292000" in output
        has_correct_female = "87,497" in output or "87497" in output
        has_correct_male = "92,382" in output or "92382" in output

        accuracy_score = sum([has_ex0, has_292000, has_correct_female, has_correct_male])

        results_summary.append({
            "config": display_name,
            "time": elapsed,
            "accuracy": f"{accuracy_score}/4",
            "ex0": "✅" if has_ex0 else "❌",
            "salary": "✅" if has_292000 else "❌",
            "female": "✅" if has_correct_female else "❌",
            "male": "✅" if has_correct_male else "❌",
        })

    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ Error after {elapsed:.2f}s: {str(e)[:200]}")
        results_summary.append({
            "config": display_name,
            "time": elapsed,
            "accuracy": "ERROR",
            "ex0": "❌",
            "salary": "❌",
            "female": "❌",
            "male": "❌",
        })

print("\n\n" + "=" * 100)
print("SUMMARY TABLE")
print("=" * 100)
print(f"{'Configuration':<45} {'Time':>8} {'Accuracy':>10} {'EX0':>5} {'$292K':>7} {'Female':>8} {'Male':>6}")
print("-" * 100)
for result in results_summary:
    print(f"{result['config']:<45} {result['time']:>7.2f}s {result['accuracy']:>10} {result['ex0']:>5} {result['salary']:>7} {result['female']:>8} {result['male']:>6}")

print("\n" + "=" * 100)
print("KEY INSIGHTS:")
print("=" * 100)
print("• Does agent_type affect OpenAI model accuracy?")
print("  Compare GPT-4.1-mini [openai-tools] vs [zero-shot-react]")
print("\n• How does Claude compare when controlling for other factors?")
print("  All models use temperature=0 and max_iterations=30")
print("=" * 100)
