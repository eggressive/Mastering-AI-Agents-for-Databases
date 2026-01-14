import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv("../database-ai-agents-main/.env")

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
