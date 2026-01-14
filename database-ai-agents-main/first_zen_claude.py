"""
Zen Master AI Agent (Claude Version)
=====================================
An interactive conversational agent that embodies the wisdom of a Zen master.
Master Kenji offers contemplative guidance using nature metaphors, koans, and paradoxes.
"""

from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

# Load environment variables from .env file
load_dotenv()

anthropic_key = os.getenv("ANTHROPIC_API_KEY")

model_name = "claude-sonnet-4-5-20250929"  # Best for philosophical discussions

# Configure model for Zen wisdom (thoughtful, contemplative responses)
model = ChatAnthropic(
    api_key=anthropic_key,
    model=model_name,
    temperature=0.8,      # Allow for creative, varied wisdom
    max_tokens=500,       # Allow for deeper reflections
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
    print("Master Kenji (Claude) awaits your questions...")
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
