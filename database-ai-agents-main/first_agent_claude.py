from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

# Load environment variables from .env file
load_dotenv()

anthropic_key = os.getenv("ANTHROPIC_API_KEY")

# Claude 3.5 Haiku is similar to gpt-4.1-mini (fast, efficient)
# Claude 3.5 Sonnet is more capable (similar to gpt-4o)
model_name = "claude-haiku-4-5-20251001"

# Configure model for Factual Q&A (consistent, accurate responses)
model = ChatAnthropic(
    api_key=anthropic_key,
    model=model_name,
    temperature=0.0,      # Deterministic responses (no creativity)
    max_tokens=300,       # Concise answers
)

messages = [
    SystemMessage(
        content="You are a helpful assistant who is extremely competent as a Computer Scientist! Your name is Rob."
    ),
    HumanMessage(content="who was the very first computer scientist?"),
]


# Test with a single question (uncomment to use):
# res = model.invoke(messages)
# print(res.content)


def first_agent(messages):
    res = model.invoke(messages)
    return res


def run_agent():
    print("Simple AI Agent (Claude): Type 'exit' to quit")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        print("AI Agent is thinking...")
        messages = [HumanMessage(content=user_input)]
        response = first_agent(messages)
        print("AI Agent: getting the response...")
        print(f"AI Agent: {response.content}")


if __name__ == "__main__":
    run_agent()
