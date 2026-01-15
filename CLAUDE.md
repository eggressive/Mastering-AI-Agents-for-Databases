# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository demonstrates building AI agents for database interactions using OpenAI's GPT and Anthropic's Claude models with LangChain. It contains multiple implementations showcasing different approaches to querying and analyzing salary data from a 2023 employee dataset, as well as conversational agents with different personalities (Zen master, computer scientist assistant).

## Setup and Environment

### Installation
```bash
cd database-ai-agents-main
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file in the `database-ai-agents-main` directory with:
```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

**API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/settings/keys

## Architecture

### Data Layer
- **Database**: SQLite database at `./db/salary.db` containing the `salaries_2023` table
- **Source Data**: CSV file at `./data/salaries_2023.csv` (928KB)
- **Schema**:
  ```sql
  CREATE TABLE salaries_2023 (
      "Department" TEXT,
      "Department_Name" TEXT,
      "Division" TEXT,
      "Gender" TEXT,
      "Base_Salary" FLOAT,
      "Overtime_Pay" FLOAT,
      "Longevity_Pay" FLOAT,
      "Grade" TEXT
  );
  ```
  View schema: `sqlite3 database-ai-agents-main/db/salary.db ".schema salaries_2023"`

### Agent Implementations

The codebase contains multiple agent implementations demonstrating different interaction patterns:

#### Database Agents
1. **csv_agent.py** - Pandas DataFrame agent with Streamlit UI for CSV analysis
2. **sql_db_agent.py** - LangChain SQL agent with Streamlit UI for natural language SQL queries
3. **use_case_classifier.py** - LLM-as-Judge use case classifier with Streamlit UI (determines if task needs automation, hybrid, or agentic approach)
4. **fun_call_db_agent.py** - Database queries using OpenAI function calling with predefined SQL functions
5. **assis_api_sql_db.py** - OpenAI Assistants API implementation with thread-based conversations

#### Conversational Agents
6. **first_agent.py** - Basic LangChain chat agent using GPT-4.1-mini (baseline example)
7. **first_agent_claude.py** - Basic chat agent using Claude Haiku 4.5
8. **first_zen.py** - Zen master personality agent using GPT-4.1-mini (temperature=0.8 for creativity)
9. **first_zen_claude.py** - Zen master personality agent using Claude Sonnet 4.5 (recommended for philosophical discussions)

#### Demo/Utilities
10. **fun_calling.py** - OpenAI function calling demo (weather example)

### Helper Modules

**helpers.py** - Database query functions and tool definitions:
- `get_avg_salary_and_female_count_for_division(division_name)`
- `get_total_overtime_pay_for_department(department_name)`
- `get_total_longevity_pay_for_grade(grade)`
- `get_employee_count_by_gender_in_department(department_name)`
- `get_employees_with_overtime_above(amount)`

These functions use SQLAlchemy with raw SQL queries (vulnerable to SQL injection - for demo purposes only).

**llm-as-judge** - Classification framework prompt:
- Contains the DSE Use Case Classification framework (V7)
- Defines evaluation criteria for determining automation approach
- Used by `use_case_classifier.py` as the judge's system prompt
- Provides structured classification into: Deterministic, Hybrid, or Agentic approaches

## Running the Applications

### Streamlit Web Interfaces

**Use Case Classifier (LLM-as-Judge)**:
```bash
cd database-ai-agents-main
streamlit run use_case_classifier.py
```
Classifies database/data service tasks into: Deterministic Automation, Hybrid Approach, or Agentic Approach.

**CSV Agent (Pandas-based analysis)**:
```bash
cd database-ai-agents-main
streamlit run csv_agent.py
```
Interactive analysis of CSV data using Pandas and natural language queries.

**SQL Agent (Natural language to SQL)**:
```bash
cd database-ai-agents-main
streamlit run sql_db_agent.py
```
Converts natural language questions into SQL queries and executes them.

### CLI Scripts

#### Database Agents
**Function calling with database**:
```bash
cd database-ai-agents-main
python fun_call_db_agent.py
```

**OpenAI Assistants API**:
```bash
cd database-ai-agents-main
python assis_api_sql_db.py
```

**Function calling demo**:
```bash
cd database-ai-agents-main
python fun_calling.py
```

#### Conversational Agents
**Basic chat agent (GPT)**:
```bash
cd database-ai-agents-main
python first_agent.py
```

**Basic chat agent (Claude)**:
```bash
cd database-ai-agents-main
python first_agent_claude.py
```

**Zen Master (Claude - Recommended)**:
```bash
cd database-ai-agents-main
python first_zen_claude.py
```

**Zen Master (GPT)**:
```bash
cd database-ai-agents-main
python first_zen.py
```

## Key Design Patterns

### Database Initialization Pattern
Most SQL-based scripts follow this initialization pattern:
```python
database_file_path = "./db/salary.db"
engine = create_engine(f"sqlite:///{database_file_path}")
df = pd.read_csv("./data/salaries_2023.csv").fillna(value=0)
df.to_sql("salaries_2023", con=engine, if_exists="replace", index=False)
```
The database is recreated from CSV on each run.

### Agent Prompt Engineering
- **sql_db_agent.py** uses custom prefix (`MSSQL_AGENT_PREFIX`) and format instructions to guide SQL generation
- **csv_agent.py** uses prefix/suffix prompts (`CSV_PROMPT_PREFIX`, `CSV_PROMPT_SUFFIX`) to ensure answer verification
- Both emphasize: never make up answers, always show SQL/calculation explanations, limit results to top_k

### Function Calling Architecture
- **helpers.py** defines tool schemas in OpenAI format (`tools_sql` array)
- Functions map to available database operations
- Used by both direct function calling and Assistants API implementations

### LLM-as-Judge Pattern
- **use_case_classifier.py** implements the LLM-as-Judge pattern
- Uses GPT-4.1-mini with temperature=0.1 for consistent, reliable evaluations
- Loads classification framework from `llm-as-judge` file
- Evaluates whether tasks should use: Deterministic Automation, Hybrid Approach, or Agentic AI
- Pattern: System prompt contains evaluation criteria, user provides use case description, LLM returns structured classification

## Model Configuration

### OpenAI Models

Agents use various GPT models depending on the use case:

**For Factual Q&A** (first_agent.py):
```python
llm_name = "gpt-4.1-mini-2025-04-14"
model = ChatOpenAI(
    api_key=openai_key,
    model=llm_name,
    temperature=0.0,      # Deterministic responses
    max_tokens=300,       # Concise answers
)
```

**For Creative/Philosophical Tasks** (first_zen.py):
```python
llm_name = "gpt-4.1-mini-2025-04-14"
model = ChatOpenAI(
    api_key=openai_key,
    model=llm_name,
    temperature=0.8,      # Allow creativity
    max_tokens=500,       # Deeper reflections
)
```

**Direct OpenAI API** (function calling, assistants):
```python
client = OpenAI(api_key=openai_key)
```

**Available OpenAI Models:**
- `gpt-4.1-mini-2025-04-14` - Fast, efficient, cost-effective
- `gpt-4o-mini` - Standard mini model
- `gpt-4o` - More capable
- `gpt-3.5-turbo` - Legacy, very cost-effective

### Anthropic Claude Models

**For Factual Q&A** (first_agent_claude.py):
```python
model_name = "claude-haiku-4-5-20251001"
model = ChatAnthropic(
    api_key=anthropic_key,
    model=model_name,
    temperature=0.0,
    max_tokens=300,
)
```

**For Philosophical Discussions** (first_zen_claude.py - Recommended):
```python
model_name = "claude-sonnet-4-5-20250929"
model = ChatAnthropic(
    api_key=anthropic_key,
    model=model_name,
    temperature=0.8,
    max_tokens=500,
)
```

**Available Claude Models:**
- `claude-haiku-4-5-20251001` - Fast and efficient
- `claude-sonnet-4-5-20250929` - Balanced, great for philosophy
- `claude-opus-4-5-20251101` - Most capable
- `claude-3-5-haiku-20241022` - Previous generation
- `claude-3-7-sonnet-20250219` - Enhanced 3.7

## Utility Scripts

**Check available OpenAI models**:
```bash
cd database-ai-agents-main
python check_models.py
```
Lists all GPT models available in your OpenAI account.

**Check available Anthropic models**:
```bash
cd database-ai-agents-main
python check_anthropic_models.py
```
Lists all Claude models available in your Anthropic account (includes Claude 4.5 series).

## Sample Questions

### Database Agents
See `questions_sql_agent.md` for example queries organized by category:
- General aggregations (average salary, employee counts)
- Department-specific queries
- Gender-based comparisons
- Grade-specific analysis
- Complex multi-condition queries

### Zen Master Agents
Example questions for philosophical exploration:
- "Master, what is the meaning of life?"
- "Master, does the dog have Buddha Nature?" (classic Zen koan)
- "What is the sound of one hand clapping?"
- "How can I find inner peace?"
- "What is the nature of reality?"
- "How do I let go of suffering?"

## Zen Master Agent Design

The Zen master agents demonstrate personality-driven AI with carefully crafted system prompts:

**System Prompt Pattern:**
```python
SystemMessage(
    content="""You are a wise Zen master who has spent decades in contemplation and meditation.
    Your name is Master Kenji. You speak with profound simplicity, often using nature metaphors,
    koans, and paradoxes to illuminate deeper truths. You guide seekers not with direct answers,
    but by helping them discover wisdom within themselves. Your responses are thoughtful, poetic,
    and sometimes begin with a moment of silence (represented by "..."). You may reference the
    sound of rain, the rustling of bamboo, or the stillness of a mountain lake to convey your
    teachings."""
)
```

**Key Configuration Differences:**
- **Temperature**: 0.8 (vs 0.0 for factual agents) - allows creative, varied wisdom
- **Max Tokens**: 500 (vs 300 for factual agents) - allows deeper philosophical exploration
- **Model Choice**: Claude Sonnet 4.5 recommended for best philosophical reasoning
- **Interactive UI**: Zen garden theme with emojis and contemplative pauses

**Why Claude Works Better for Zen Master:**
- Superior philosophical reasoning
- Better with metaphorical language
- More nuanced understanding of Eastern philosophy
- Longer, more thoughtful responses

## Important Notes

### Database
- The database is SQLite-based and recreated from CSV on each agent run (not persistent)
- SQL queries in helpers.py use string formatting (SQL injection vulnerable - demo code)
- All database agents operate on the same `salaries_2023` table structure
- Streamlit apps run on default port 8501

### Dependencies
- Core: `langchain==0.3.13`, `langchain-core==0.3.28`
- OpenAI: `openai==1.58.1`, `langchain-openai==0.2.14`
- Anthropic: `langchain-anthropic==0.2.4`
- Web UI: `streamlit==1.41.1`
- Data: `pandas==2.2.3`, `SQLAlchemy==2.0.36`

### Virtual Environment
All scripts should be run from within the virtual environment:
```bash
cd database-ai-agents-main
source venv/bin/activate
python <script_name>.py
```

### Agent Comparison Files
- `CLAUDE_vs_GPT.md` - Detailed comparison of OpenAI and Anthropic models
- Both OpenAI and Claude versions of agents use the same LangChain interfaces
- Choose model based on use case: GPT for cost-efficiency, Claude for reasoning/philosophy
