"""
Agent Type Comparison Demo
Shows the difference between zero-shot-react-description and openai-tools
with verbose mode enabled to see the reasoning process
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import time

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# Load data
df = pd.read_csv("./data/salaries_2023.csv").fillna(value=0)

# Use a simpler question for clearer demonstration
SIMPLE_QUESTION = "What is the average base salary?"

# Use GPT-4.1-mini for consistency
MODEL_NAME = "gpt-4.1-mini-2025-04-14"

def run_with_agent_type(agent_type, question):
    """Run query with specified agent type and return timing + output"""
    print(f"\n{'='*100}")
    print(f"AGENT TYPE: {agent_type}")
    print(f"{'='*100}\n")

    model = ChatOpenAI(api_key=openai_key, model=MODEL_NAME, temperature=0)

    agent = create_pandas_dataframe_agent(
        llm=model,
        df=df,
        agent_type=agent_type,
        verbose=True,  # ← Key difference: shows reasoning process
        allow_dangerous_code=True,
        max_iterations=15,  # Reduced for simpler demo
    )

    print(f"🤖 Model: {MODEL_NAME}")
    print(f"📋 Agent Type: {agent_type}")
    print(f"❓ Question: {question}\n")
    print("-" * 100)

    start_time = time.time()
    try:
        result = agent.invoke(question)
        elapsed = time.time() - start_time

        print("-" * 100)
        print(f"\n⏱️  Time taken: {elapsed:.2f}s")
        print(f"\n✅ Final Answer:")
        print(result['output'])

        return elapsed, result['output'], None

    except Exception as e:
        elapsed = time.time() - start_time
        print("-" * 100)
        print(f"\n❌ Error after {elapsed:.2f}s: {str(e)}")
        return elapsed, None, str(e)


def main():
    print("\n" + "█" * 100)
    print("█" + " " * 98 + "█")
    print("█" + " " * 30 + "AGENT TYPE COMPARISON DEMO" + " " * 42 + "█")
    print("█" + " " * 98 + "█")
    print("█" * 100)

    print("\n📊 This demo compares two agent types with VERBOSE mode enabled:")
    print("   1. zero-shot-react-description (Traditional ReAct pattern)")
    print("   2. openai-tools (Modern function calling)")
    print("\n💡 Watch for:")
    print("   • How each agent 'thinks' (Thought: ...)")
    print("   • How they invoke tools (Action: ... vs function calls)")
    print("   • Number of steps taken")
    print("   • Speed difference")

    # Test 1: zero-shot-react-description
    time1, output1, error1 = run_with_agent_type("zero-shot-react-description", SIMPLE_QUESTION)

    # Small pause for readability
    time.sleep(1)

    # Test 2: openai-tools
    time2, output2, error2 = run_with_agent_type("openai-tools", SIMPLE_QUESTION)

    # Summary comparison
    print("\n\n" + "█" * 100)
    print("█" + " " * 40 + "COMPARISON SUMMARY" + " " * 40 + "█")
    print("█" * 100)

    print(f"\n{'Agent Type':<35} {'Time':>12} {'Status':>15} {'Correct Answer':>20}")
    print("-" * 100)

    status1 = "✅ Success" if not error1 else "❌ Error"
    status2 = "✅ Success" if not error2 else "❌ Error"

    # Check if answers are correct (should be around $90,312)
    correct1 = "✅" if output1 and "90,312" in output1 else "⚠️"
    correct2 = "✅" if output2 and "90,312" in output2 else "⚠️"

    print(f"{'zero-shot-react-description':<35} {f'{time1:.2f}s':>12} {status1:>15} {correct1:>20}")
    print(f"{'openai-tools':<35} {f'{time2:.2f}s':>12} {status2:>15} {correct2:>20}")

    if not error1 and not error2:
        speedup = time1 / time2
        print(f"\n⚡ Speed difference: openai-tools is {speedup:.2f}x faster")

    print("\n" + "█" * 100)
    print("KEY OBSERVATIONS:")
    print("█" * 100)
    print("""
1. ZERO-SHOT-REACT FORMAT:
   • Uses explicit "Thought:", "Action:", "Action Input:", "Observation:" format
   • Shows step-by-step reasoning process
   • Each step is a separate message exchange
   • More verbose and educational
   • Slower due to multiple reasoning steps

2. OPENAI-TOOLS FORMAT:
   • Uses structured function calling (JSON format)
   • Less explicit reasoning shown
   • More efficient message exchanges
   • Faster execution
   • Better for production

3. ACCURACY:
   • Both should produce correct answers
   • Difference is mainly in HOW they get there, not WHAT they conclude

4. WHEN TO USE:
   • zero-shot-react: Debugging, learning, complex reasoning
   • openai-tools: Production, speed-critical applications
""")
    print("█" * 100)


if __name__ == "__main__":
    main()
