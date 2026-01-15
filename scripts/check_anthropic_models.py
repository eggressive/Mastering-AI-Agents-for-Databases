"""
Check available Anthropic Claude models.

This script loads environment variables from a .env file. It searches for .env in:
1. Current working directory
2. Parent and grandparent directories
3. database-ai-agents-main subdirectory (if it exists)
4. Default load_dotenv() behavior (searches up directory tree)

The .env file should contain:
    ANTHROPIC_API_KEY=your_api_key_here

Usage:
    python check_anthropic_models.py
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic


def find_and_load_dotenv():
    """
    Search for .env file in multiple locations and load it.
    Prints the location if found in explicit search paths.
    """
    # List of paths to search for .env file
    search_paths = [
        Path.cwd() / ".env",  # Current directory
        Path.cwd().parent / ".env",  # Parent directory
        Path.cwd().parent.parent / ".env",  # Grandparent directory
        Path.cwd() / "database-ai-agents-main" / ".env",  # Subdirectory
        Path.cwd().parent / "database-ai-agents-main" / ".env",  # Parent's subdirectory
    ]
    
    for env_path in search_paths:
        if env_path.exists():
            load_dotenv(env_path)
            print(f"Loaded environment from: {env_path}")
            return
    
    # Try default load_dotenv() which searches up the directory tree
    load_dotenv()


# Load environment variables
find_and_load_dotenv()

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
