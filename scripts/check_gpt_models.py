"""
Check available OpenAI GPT models.

This script loads environment variables from a .env file. It searches for .env in:
1. Script's directory
2. Repository root (parent of scripts/)
3. Grandparent directory (in case script is nested deeper)
4. database-ai-agents-main subdirectory relative to repo root

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
    Anchored to script's directory to avoid loading unrelated .env files.
    """
    # Anchor search to script's directory, not caller's cwd
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent  # Assume scripts/ is one level below repo root
    
    # List of paths to search for .env file
    search_paths = [
        script_dir / ".env",  # Script's directory
        repo_root / ".env",  # Repository root
        repo_root.parent / ".env",  # Grandparent (if repo is nested)
        repo_root / "database-ai-agents-main" / ".env",  # Subdirectory
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
