# Agent Quick Reference Guide

A comprehensive guide to all AI agents in this repository.

## Table of Contents
- [Streamlit Web Applications](#streamlit-web-applications)
- [Database Agents (CLI)](#database-agents-cli)
- [Conversational Agents](#conversational-agents)
- [Demo/Utilities](#demoutilities)
- [Model Comparison](#model-comparison)

---

## Streamlit Web Applications

### 🔍 Use Case Classifier
**File:** `use_case_classifier.py`
**Purpose:** LLM-as-Judge pattern to classify database/data service tasks
**Model:** GPT-4.1-mini (temperature=0.1 for consistency)
**Run:**
```bash
cd database-ai-agents-main
streamlit run use_case_classifier.py
```

**What it does:**
- Classifies tasks into: Deterministic Automation, Hybrid Approach, or Agentic AI
- Uses DSE Use Case Classification framework (V7)
- Provides structured recommendations

**When to use:**
- Planning a new database/data service task
- Deciding whether to use traditional automation or AI agents
- Understanding complexity of a use case

---

### 📊 CSV Agent
**File:** `csv_agent.py`
**Purpose:** Interactive analysis of CSV data using Pandas
**Model:** GPT-3.5-turbo
**Run:**
```bash
cd database-ai-agents-main
streamlit run csv_agent.py
```

**What it does:**
- Natural language queries on CSV data
- Uses Pandas DataFrame agent
- Verifies answers using prefix/suffix prompts
- Shows calculation explanations

**Features:**
- Dataset preview
- Custom prompt engineering for accuracy
- Markdown-formatted results

**When to use:**
- Quick CSV data analysis
- Non-technical users need to query data
- Exploratory data analysis

---

### 💾 SQL Agent
**File:** `sql_db_agent.py`
**Purpose:** Convert natural language to SQL queries
**Model:** GPT-3.5-turbo
**Run:**
```bash
cd database-ai-agents-main
streamlit run sql_db_agent.py
```

**What it does:**
- Converts questions to SQL
- Executes queries on salaries_2023 table
- Shows SQL query used
- Limits results to top_k (default: 30)

**Features:**
- Custom MSSQL_AGENT_PREFIX prompt
- Format instructions for consistent output
- Automatic query validation

**When to use:**
- Natural language database queries
- Learning SQL (shows generated queries)
- Quick database exploration

---

## Database Agents (CLI)

### 🔧 Function Calling Database Agent
**File:** `fun_call_db_agent.py`
**Purpose:** Database queries using OpenAI function calling
**Model:** GPT-3.5-turbo
**Run:**
```bash
cd database-ai-agents-main
python fun_call_db_agent.py
```

**What it does:**
- Uses predefined functions from helpers.py
- OpenAI function calling API
- Structured data retrieval

**Available functions:**
- `get_avg_salary_and_female_count_for_division()`
- `get_total_overtime_pay_for_department()`
- `get_total_longevity_pay_for_grade()`
- `get_employee_count_by_gender_in_department()`
- `get_employees_with_overtime_above()`

**When to use:**
- Controlled function execution
- Specific query patterns
- Learning OpenAI function calling

---

### 🤖 OpenAI Assistants API Agent
**File:** `assis_api_sql_db.py`
**Purpose:** Thread-based conversational database queries
**Model:** GPT-3.5-turbo
**Run:**
```bash
cd database-ai-agents-main
python assis_api_sql_db.py
```

**What it does:**
- Uses OpenAI Assistants API
- Maintains conversation threads
- Function calling with database

**Features:**
- Stateful conversations
- Thread management
- Tool execution tracking

**When to use:**
- Multi-turn conversations
- Maintaining context across queries
- Learning Assistants API

---

## Conversational Agents

### 💬 Basic Chat Agent (GPT)
**File:** `first_agent.py`
**Purpose:** Baseline conversational agent for factual Q&A
**Model:** GPT-4.1-mini
**Configuration:** temperature=0.0, max_tokens=300
**Run:**
```bash
cd database-ai-agents-main
python first_agent.py
```

**What it does:**
- Interactive CLI chat
- Factual, consistent responses
- No conversation memory (stateless)

**When to use:**
- Testing OpenAI integration
- Simple Q&A tasks
- Baseline comparison

---

### 💬 Basic Chat Agent (Claude)
**File:** `first_agent_claude.py`
**Purpose:** Baseline conversational agent using Claude
**Model:** Claude Haiku 4.5
**Configuration:** temperature=0.0, max_tokens=300
**Run:**
```bash
cd database-ai-agents-main
python first_agent_claude.py
```

**What it does:**
- Same as GPT version but uses Claude
- Interactive CLI chat
- Factual responses

**When to use:**
- Testing Anthropic integration
- Comparing Claude vs GPT
- Cost-effective Claude option

---

### 🧘 Zen Master (GPT)
**File:** `first_zen.py`
**Purpose:** Wise Zen master personality for philosophical guidance
**Model:** GPT-4.1-mini
**Configuration:** temperature=0.8, max_tokens=500
**Run:**
```bash
cd database-ai-agents-main
python first_zen.py
```

**Personality:**
- Master Kenji - wise Zen master
- Uses nature metaphors and koans
- Guides seekers to discover wisdom within

**What it does:**
- Philosophical discussions
- Creative, varied responses
- Beautiful Zen garden UI with emojis

**Example questions:**
- "Master, what is the meaning of life?"
- "What is the sound of one hand clapping?"
- "How can I find inner peace?"

**When to use:**
- Philosophical exploration
- Learning creative prompt engineering
- Testing personality-driven agents

---

### 🧘 Zen Master (Claude) ⭐ RECOMMENDED
**File:** `first_zen_claude.py`
**Purpose:** Wise Zen master using Claude (best for philosophy)
**Model:** Claude Sonnet 4.5
**Configuration:** temperature=0.8, max_tokens=500
**Run:**
```bash
cd database-ai-agents-main
python first_zen_claude.py
```

**Why recommended:**
- Superior philosophical reasoning
- Better with metaphorical language
- More nuanced understanding of Eastern philosophy
- Longer, more thoughtful responses

**Example response quality:**
```
When asked: "Does the dog have Buddha Nature?"

Master Kenji responds with the classic "Mu!" koan,
references Zhaozhou, and guides you to discover
the answer within through metaphor and questioning.
```

**When to use:**
- Philosophical discussions (best option)
- Learning personality agents
- Demonstrating Claude's capabilities

---

## Demo/Utilities

### ☁️ Function Calling Demo
**File:** `fun_calling.py`
**Purpose:** Demonstrate OpenAI function calling (weather example)
**Model:** GPT-4o
**Run:**
```bash
cd database-ai-agents-main
python fun_calling.py
```

**What it does:**
- Simple weather query example
- Shows function calling pattern
- Hardcoded weather data

**When to use:**
- Learning function calling basics
- Template for new function calling agents
- Testing OpenAI API

---

## Model Comparison

### OpenAI Models

| Model | Speed | Cost | Best For |
|-------|-------|------|----------|
| gpt-4.1-mini | ⚡⚡⚡ | 💰 | Factual Q&A, cost-effective |
| gpt-4o-mini | ⚡⚡⚡ | 💰 | General purpose, efficient |
| gpt-4o | ⚡⚡ | 💰💰 | Complex reasoning |
| gpt-3.5-turbo | ⚡⚡⚡ | 💰 | Legacy apps, very cheap |

### Anthropic Claude Models

| Model | Speed | Cost | Best For |
|-------|-------|------|----------|
| claude-haiku-4-5 | ⚡⚡⚡ | 💰💰 | Fast, efficient |
| claude-sonnet-4-5 | ⚡⚡ | 💰💰💰 | Balanced, philosophy ⭐ |
| claude-opus-4-5 | ⚡ | 💰💰💰💰 | Maximum capability |
| claude-3-5-haiku | ⚡⚡⚡ | 💰💰 | Previous gen, still good |

### When to Choose What

**Choose GPT when:**
- Cost is the primary concern
- You need the fastest response time
- Task is straightforward factual Q&A

**Choose Claude when:**
- Task involves philosophical reasoning
- Need better handling of metaphorical language
- Longer context windows needed (up to 200K tokens)
- More nuanced understanding required

---

## Configuration Patterns

### Factual Q&A Configuration
```python
temperature=0.0      # Deterministic, consistent
max_tokens=300       # Concise answers
```

### Creative/Philosophical Configuration
```python
temperature=0.8      # Allow creativity and variation
max_tokens=500       # Allow deeper exploration
```

### Evaluation/Classification Configuration
```python
temperature=0.1      # Consistent evaluations, minimal randomness
max_tokens=2000      # Detailed explanations
```

---

## Quick Start Commands

```bash
# Set up environment
cd database-ai-agents-main
source venv/bin/activate

# Streamlit apps (web UI)
streamlit run use_case_classifier.py
streamlit run csv_agent.py
streamlit run sql_db_agent.py

# CLI agents
python first_agent.py              # GPT chat
python first_agent_claude.py       # Claude chat
python first_zen_claude.py         # Zen master (recommended)

# Database agents
python fun_call_db_agent.py        # Function calling
python assis_api_sql_db.py         # Assistants API

# Demo
python fun_calling.py              # Function calling demo
```

---

## Environment Setup

Required in `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

---

## Agent Selection Flowchart

```
Need database queries?
├─ Yes → Need web UI?
│   ├─ Yes → Need classification? → use_case_classifier.py
│   │        Need CSV analysis? → csv_agent.py
│   │        Need SQL queries? → sql_db_agent.py
│   └─ No → Want function calling? → fun_call_db_agent.py
│            Want threads? → assis_api_sql_db.py
│
└─ No → Need personality/philosophy?
    ├─ Yes → first_zen_claude.py (⭐ recommended)
    │        first_zen.py (GPT alternative)
    └─ No → Basic chat?
            first_agent_claude.py (Claude)
            first_agent.py (GPT)
```

---

## Notes

- All database agents use `salaries_2023` table (recreated from CSV on each run)
- Streamlit apps run on port 8501
- CLI agents are stateless (no conversation memory)
- SQL queries in helpers.py are vulnerable to SQL injection (demo code only)
- Always activate virtual environment before running scripts

---

## Resources

- **OpenAI API Keys:** https://platform.openai.com/api-keys
- **Anthropic API Keys:** https://console.anthropic.com/settings/keys
- **LangChain Docs:** https://python.langchain.com/
- **Streamlit Docs:** https://docs.streamlit.io/

---

*Last updated: Based on codebase as of January 2026*
