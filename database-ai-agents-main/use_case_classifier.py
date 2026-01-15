"""
Use Case Classifier - LLM as Judge Implementation

This tool helps users determine whether their database/data systems task
should be handled with:
- Deterministic Automation (scripts, workflows)
- Hybrid Approach (rules + ML augmentation)
- Agentic Approach (AI reasoning required)

Uses the DSE Use Case Classification framework (V7) as the judge prompt.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import streamlit as st

# Load environment variables
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

# Use a capable model for nuanced evaluation
llm_name = "gpt-4.1-mini-2025-04-14"

model = ChatOpenAI(
    api_key=openai_key,
    model=llm_name,
    temperature=0.1,  # Low temperature for consistent evaluations
    max_tokens=2000,
)

# Load the judge prompt from file
def load_judge_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), "llm-as-judge")
    with open(prompt_path, "r") as f:
        return f.read()

JUDGE_PROMPT = load_judge_prompt()


def classify_use_case(use_case_description: str) -> str:
    """
    Classify a use case using the LLM-as-Judge framework.

    Args:
        use_case_description: Description of the database/data systems task

    Returns:
        Classification result with scores and recommendations
    """
    # Replace the placeholder in the judge prompt
    full_prompt = JUDGE_PROMPT.replace("{USE_CASE_DESCRIPTION}", use_case_description)

    messages = [
        SystemMessage(content="You are an expert evaluator for Data Systems Engineering use cases. Follow the instructions precisely and provide rigorous, unbiased scoring."),
        HumanMessage(content=full_prompt)
    ]

    response = model.invoke(messages)
    return response.content


# Streamlit UI
st.set_page_config(
    page_title="Use Case Classifier",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ DSE Use Case Classifier")
st.markdown("""
**LLM-as-Judge for Database & Data Systems Tasks**

Describe your database or data systems task below, and the AI judge will classify
whether it needs:
- **Deterministic Automation** (7-14 points): Scripts, workflows, rule-based systems
- **Hybrid Approach** (15-21 points): Deterministic core + ML augmentation
- **Agentic Approach** (22-35 points): AI reasoning and adaptation required
""")

st.divider()

# Example use cases for quick testing
with st.expander("📝 Example Use Cases (click to expand)"):
    st.markdown("""
    **Example 1 - Likely Deterministic:**
    > "Automatically archive database records older than 2 years to cold storage every night at 2 AM,
    > following our data retention policy."

    **Example 2 - Likely Hybrid:**
    > "Monitor database query performance and automatically identify slow queries that exceed
    > baseline thresholds, then suggest index improvements."

    **Example 3 - Likely Agentic:**
    > "Analyze our database logs and explain to stakeholders why query performance degraded
    > last week, identifying root causes and recommending architectural changes."
    """)

# Input area
use_case = st.text_area(
    "Describe your database/data systems task:",
    height=150,
    placeholder="Example: Create an automated system that monitors replication lag across our database clusters and triggers alerts when thresholds are exceeded..."
)

col1, col2 = st.columns([1, 4])

with col1:
    classify_button = st.button("🔍 Classify", type="primary", use_container_width=True)

with col2:
    clear_button = st.button("Clear", use_container_width=False)

if clear_button:
    st.rerun()

if classify_button:
    if not use_case.strip():
        st.error("Please enter a use case description.")
    elif not openai_key:
        st.error("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
    else:
        with st.spinner("🤔 Analyzing use case with LLM Judge..."):
            try:
                result = classify_use_case(use_case)

                st.divider()
                st.subheader("📊 Classification Result")
                st.markdown(result)

            except Exception as e:
                st.error(f"Error during classification: {str(e)}")

# Footer
st.divider()
st.caption("Built with LLM-as-Judge pattern | Uses DSE Classification Framework V7")
