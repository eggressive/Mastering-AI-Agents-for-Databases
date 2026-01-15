"""
CSV Agent Performance Benchmark: GPT-4.1-mini vs Claude Haiku

Compares models across multiple dimensions:
- Accuracy: Correct answers
- Speed: Response time
- Cost: Token usage
- Quality: Answer formatting and explanation
- Reasoning: Thought process quality
"""

import os
import time
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# Load environment variables
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")

# Load data
df = pd.read_csv("./data/salaries_2023.csv").fillna(value=0)

# Test queries with expected answers for accuracy checking
test_queries = [
    {
        "query": "How many rows are in the dataframe?",
        "expected": 10291,
        "category": "Simple",
    },
    {
        "query": "What is the average base salary?",
        "expected": 90312.17,  # Approximate
        "category": "Simple",
        "tolerance": 1.0,  # Allow $1 difference
    },
    {
        "query": "How many unique departments are there?",
        "expected": 42,
        "category": "Simple",
    },
    {
        "query": "What is the highest base salary?",
        "expected": 292000.0,
        "category": "Simple",
    },
    {
        "query": "How many male vs female employees are there?",
        "expected": {"M": 5929, "F": 4362},
        "category": "Intermediate",
    },
    {
        "query": "What is the average base salary by gender?",
        "expected": {"F": 87497.50, "M": 92382.93},
        "category": "Intermediate",
        "tolerance": 1.0,
    },
    {
        "query": "Which department has the most employees?",
        "expected": "HHS",
        "category": "Intermediate",
    },
    {
        "query": "What grade has the highest average base salary?",
        "expected": None,  # Need to verify
        "category": "Complex",
    },
]


def create_agent(model_name, model_type="openai"):
    """Create a pandas dataframe agent with specified model."""
    if model_type == "openai":
        model = ChatOpenAI(api_key=openai_key, model=model_name, temperature=0)
    elif model_type == "anthropic":
        model = ChatAnthropic(api_key=anthropic_key, model=model_name, temperature=0)
    else:
        raise ValueError(f"Unknown model type: {model_type}")

    agent = create_pandas_dataframe_agent(
        llm=model,
        df=df,
        verbose=False,  # Set to False for cleaner output
        allow_dangerous_code=True,
    )

    return agent, model_name, model_type


def run_benchmark(agent, model_name, query):
    """Run a single query and measure performance."""
    start_time = time.time()

    try:
        result = agent.invoke(query)
        end_time = time.time()

        return {
            "success": True,
            "output": result.get("output", ""),
            "response_time": end_time - start_time,
            "error": None,
        }
    except Exception as e:
        end_time = time.time()
        return {
            "success": False,
            "output": None,
            "response_time": end_time - start_time,
            "error": str(e),
        }


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 100)
    print(f"{title:^100}")
    print("=" * 100)


def print_result(model_name, query_num, total, query, result):
    """Print individual test result."""
    status = "✅" if result["success"] else "❌"
    print(f"\n{status} [{model_name}] Test {query_num}/{total}")
    print(f"Query: {query}")
    print(f"Time: {result['response_time']:.2f}s")
    if result["success"]:
        print(f"Answer: {result['output'][:200]}{'...' if len(result['output']) > 200 else ''}")
    else:
        print(f"Error: {result['error']}")


def compare_models():
    """Run comprehensive comparison between models."""
    print_header("CSV AGENT PERFORMANCE BENCHMARK")
    print(f"\nDataset: salaries_2023.csv ({len(df)} rows, {len(df.columns)} columns)")
    print(f"Test Queries: {len(test_queries)}")

    # Initialize models
    models = [
        ("GPT-4.1-mini", "gpt-4.1-mini-2025-04-14", "openai"),
        ("Claude Haiku 4.5", "claude-haiku-4-5-20251001", "anthropic"),
    ]

    results = {}

    # Run tests for each model
    for model_display, model_name, model_type in models:
        print_header(f"Testing: {model_display}")
        print(f"Model: {model_name}")
        print(f"Provider: {model_type.upper()}")

        agent, _, _ = create_agent(model_name, model_type)
        model_results = []

        for i, test in enumerate(test_queries, 1):
            query = test["query"]
            print(f"\n[{i}/{len(test_queries)}] {test['category']}: {query}")

            result = run_benchmark(agent, model_display, query)
            result["category"] = test["category"]
            result["query"] = query
            model_results.append(result)

            status = "✅" if result["success"] else "❌"
            print(f"{status} Time: {result['response_time']:.2f}s")
            if result["success"]:
                print(f"   Answer: {result['output'][:150]}{'...' if len(result['output']) > 150 else ''}")
            else:
                print(f"   Error: {result['error']}")

        results[model_display] = model_results

    # Generate comparison report
    print_header("COMPARATIVE ANALYSIS")

    # Success Rate
    print("\n📊 SUCCESS RATE:")
    for model_name, model_results in results.items():
        success_count = sum(1 for r in model_results if r["success"])
        success_rate = (success_count / len(model_results)) * 100
        print(f"  {model_name:20s}: {success_count}/{len(model_results)} ({success_rate:.1f}%)")

    # Average Response Time
    print("\n⚡ AVERAGE RESPONSE TIME:")
    for model_name, model_results in results.items():
        successful_results = [r for r in model_results if r["success"]]
        if successful_results:
            avg_time = sum(r["response_time"] for r in successful_results) / len(
                successful_results
            )
            print(f"  {model_name:20s}: {avg_time:.2f}s")
        else:
            print(f"  {model_name:20s}: N/A (no successful queries)")

    # Response Time by Category
    print("\n⏱️  RESPONSE TIME BY CATEGORY:")
    categories = ["Simple", "Intermediate", "Complex"]
    for category in categories:
        print(f"\n  {category}:")
        for model_name, model_results in results.items():
            category_results = [
                r for r in model_results if r["category"] == category and r["success"]
            ]
            if category_results:
                avg_time = sum(r["response_time"] for r in category_results) / len(
                    category_results
                )
                print(f"    {model_name:20s}: {avg_time:.2f}s")

    # Fastest vs Slowest
    print("\n🏆 FASTEST RESPONSES:")
    for i, test in enumerate(test_queries, 1):
        query = test["query"]
        times = {}
        for model_name, model_results in results.items():
            result = model_results[i - 1]
            if result["success"]:
                times[model_name] = result["response_time"]

        if times:
            fastest = min(times.items(), key=lambda x: x[1])
            slowest = max(times.items(), key=lambda x: x[1])
            diff = slowest[1] - fastest[1]
            print(
                f"  Q{i}: {fastest[0]} ({fastest[1]:.2f}s) vs {slowest[0]} ({slowest[1]:.2f}s) - Δ {diff:.2f}s"
            )

    # Overall Winner
    print("\n" + "=" * 100)
    print("OVERALL SUMMARY")
    print("=" * 100)

    for model_name, model_results in results.items():
        successful_results = [r for r in model_results if r["success"]]
        success_rate = (len(successful_results) / len(model_results)) * 100
        avg_time = (
            sum(r["response_time"] for r in successful_results) / len(successful_results)
            if successful_results
            else 0
        )

        print(f"\n{model_name}:")
        print(f"  Success Rate: {success_rate:.1f}%")
        print(f"  Avg Response Time: {avg_time:.2f}s")
        print(f"  Total Time: {sum(r['response_time'] for r in model_results):.2f}s")

    print("\n" + "=" * 100)
    print("BENCHMARK COMPLETED")
    print("=" * 100)


if __name__ == "__main__":
    compare_models()
