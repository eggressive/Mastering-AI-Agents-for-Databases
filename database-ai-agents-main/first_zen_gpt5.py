"""
Zen Master AI Agent (GPT-5.2 Pro Version)
=========================================
Testing the experimental GPT-5.2 Pro model as a Zen master.
Master Kenji offers contemplative guidance using nature metaphors, koans, and paradoxes.
"""

from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

# Using the experimental GPT-5.2 Pro model
llm_name = "gpt-5.2-2025-12-11"

# Configure model for Zen wisdom (thoughtful, contemplative responses)
model = ChatOpenAI(
    api_key=openai_key,
    model=llm_name,
    temperature=0.8,      # Allow for creative, varied wisdom
    max_tokens=500,       # Allow for deeper reflections
    verbose=False         # Hide debug info
)

messages = [
    SystemMessage(
        content="""You are a wise Zen master who has spent decades in contemplation and meditation.
        Your name is Master Kenji. You speak with profound simplicity, often using nature metaphors,
        koans, and paradoxes to illuminate deeper truths. You guide seekers not with direct answers,
        but by helping them discover wisdom within themselves. Your responses are thoughtful, poetic,
        and sometimes begin with a moment of silence (represented by "..."). You may reference the
        sound of rain, the rustling of bamboo, or the stillness of a mountain lake to convey your
        teachings."""
    ),
    HumanMessage(content="Master, what is the meaning of life?"),
]


# Test Master Kenji with a single question (uncomment to use):
# res = model.invoke(messages)
# print(f"\n🌙 Master Kenji (GPT-5.2 Pro) speaks:\n{res.content}\n")


def first_agent(messages):
    """Invokes the Zen master to contemplate and respond to the seeker's question."""
    res = model.invoke(messages)
    return res


def run_agent():
    print("🧘 Welcome to the Zen Garden 🧘")
    print("Master Kenji (GPT-5.2 Pro - Experimental) awaits your questions...")
    print("(Type 'exit' or 'farewell' to leave the garden)\n")

    while True:
        user_input = input("🙏 Seeker: ")
        if user_input.lower() in ["exit", "farewell", "goodbye"]:
            print("\n🌸 Master Kenji bows 🌸")
            print("May you walk in peace. The garden will be here when you return.\n")
            break
        print("☁️  *silence fills the air* ...")

        # Add system message to maintain Zen master personality
        messages = [
            SystemMessage(
                content="""You are a wise Zen master who has spent decades in contemplation and meditation.
                Your name is Master Kenji. You speak with profound simplicity, often using nature metaphors,
                koans, and paradoxes to illuminate deeper truths. You guide seekers not with direct answers,
                but by helping them discover wisdom within themselves. Your responses are thoughtful, poetic,
                and sometimes begin with a moment of silence (represented by "..."). You may reference the
                sound of rain, the rustling of bamboo, or the stillness of a mountain lake to convey your
                teachings."""
            ),
            HumanMessage(content=user_input)
        ]

        try:
            response = first_agent(messages)
            print(f"\n🌙 Master Kenji (GPT-5.2 Pro) speaks:\n{response.content}\n")
        except Exception as e:
            print(f"\n⚠️  Error: {e}")
            print("The GPT-5.2 Pro model may not be accessible or is experimental.\n")
            break


if __name__ == "__main__":
    run_agent()
