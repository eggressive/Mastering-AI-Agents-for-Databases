import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables from .env file
load_dotenv()

anthropic_key = os.getenv("ANTHROPIC_API_KEY")

if not anthropic_key:
    print("Error: ANTHROPIC_API_KEY not found in .env file")
    exit(1)

client = Anthropic(api_key=anthropic_key)

print("Fetching available models from your Anthropic account...\n")

try:
    models = client.models.list()

    print(f"Found {len(models.data)} Anthropic models:\n")
    print("-" * 80)

    for model in sorted(models.data, key=lambda x: x.id):
        print(f"  {model.id}")
        if hasattr(model, 'display_name'):
            print(f"    Display Name: {model.display_name}")
        if hasattr(model, 'max_tokens'):
            print(f"    Max Tokens: {model.max_tokens:,}")
        print()

    print("-" * 80)
    print(f"\nTotal models: {len(models.data)}")

    # Group by series
    print("\n" + "=" * 80)
    print("MODELS BY SERIES:")
    print("=" * 80)

    claude_35 = [m for m in models.data if 'claude-3-5' in m.id]
    claude_3 = [m for m in models.data if 'claude-3-' in m.id and 'claude-3-5' not in m.id]
    others = [m for m in models.data if 'claude-3' not in m.id]

    if claude_35:
        print(f"\nClaude 3.5 Series ({len(claude_35)} models):")
        for m in claude_35:
            print(f"  • {m.id}")

    if claude_3:
        print(f"\nClaude 3 Series ({len(claude_3)} models):")
        for m in claude_3:
            print(f"  • {m.id}")

    if others:
        print(f"\nOther Models ({len(others)} models):")
        for m in others:
            print(f"  • {m.id}")

except Exception as e:
    print(f"Error fetching models: {e}")
    print(f"\nNote: Anthropic API might not have a models.list() endpoint.")
    print("Here are the known Claude models as of January 2025:\n")

    known_models = {
        "Claude 3.5 (Latest)": [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022",
        ],
        "Claude 3": [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
        ],
        "Claude 2": [
            "claude-2.1",
            "claude-2.0",
        ],
    }

    print("-" * 80)
    for series, models in known_models.items():
        print(f"\n{series}:")
        for model in models:
            print(f"  • {model}")
    print("-" * 80)

    print("\n📘 Model Recommendations:")
    print("  Fast & Efficient:  claude-3-5-haiku-20241022")
    print("  Balanced:          claude-3-5-sonnet-20241022")
    print("  Most Capable:      claude-3-opus-20240229")
