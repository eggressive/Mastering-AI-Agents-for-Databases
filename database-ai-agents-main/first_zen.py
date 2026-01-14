"""
Zen Master AI Agent
====================
An interactive conversational agent that embodies the wisdom of a Zen master.
Master Kenji offers contemplative guidance using nature metaphors, koans, and paradoxes.
"""

from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

llm_name = "gpt-4.1-mini-2025-04-14"

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
# print(f"\n🌙 Master Kenji speaks:\n{res.content}\n")


def first_agent(messages):
    """Invokes the Zen master to contemplate and respond to the seeker's question."""
    res = model.invoke(messages)
    return res


def run_agent():
    print("🧘 Welcome to the Zen Garden 🧘")
    print("Master Kenji awaits your questions...")
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

        response = first_agent(messages)
        print(f"\n🌙 Master Kenji speaks:\n{response.content}\n")


if __name__ == "__main__":
    run_agent()
