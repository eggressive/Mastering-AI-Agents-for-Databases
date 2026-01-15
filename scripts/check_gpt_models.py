"""
Check available OpenAI GPT models.

This script loads environment variables from a .env file. It searches for .env in:
1. Current working directory
2. Parent and grandparent directories
3. database-ai-agents-main subdirectory (if it exists)
4. Default load_dotenv() behavior (searches up directory tree)

The .env file should contain:
    OPENAI_API_KEY=your_api_key_here

Usage:
    python check_gpt_models.py
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


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

openai_key = os.getenv("OPENAI_API_KEY")

if not openai_key:
    print("Error: OPENAI_API_KEY not found in .env file")
    exit(1)

client = OpenAI(api_key=openai_key)

print("Fetching available models from your OpenAI account...\n")

try:
    models = client.models.list()

    # Filter for GPT models only
    gpt_models = [model for model in models.data if 'gpt' in model.id.lower()]

    print(f"Found {len(gpt_models)} GPT models:\n")
    print("-" * 60)

    for model in sorted(gpt_models, key=lambda x: x.id):
        print(f"  {model.id}")

    print("-" * 60)
    print(f"\nTotal GPT models: {len(gpt_models)}")

except Exception as e:
    print(f"Error fetching models: {e}")
