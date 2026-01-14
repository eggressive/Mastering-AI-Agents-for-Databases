# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository demonstrates building AI agents for database interactions using OpenAI's GPT models and LangChain. It contains multiple implementations showcasing different approaches to querying and analyzing salary data from a 2023 employee dataset.

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
```

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

The codebase contains five distinct agent implementations, each demonstrating different interaction patterns:

1. **first_agent.py** - Basic LangChain chat agent (baseline example)
2. **csv_agent.py** - Pandas DataFrame agent with Streamlit UI for CSV analysis
3. **sql_db_agent.py** - LangChain SQL agent with Streamlit UI for natural language SQL queries
4. **fun_calling.py** - OpenAI function calling demo (weather example)
5. **fun_call_db_agent.py** - Database queries using OpenAI function calling with predefined SQL functions
6. **assis_api_sql_db.py** - OpenAI Assistants API implementation with thread-based conversations

### Helper Module (helpers.py)

Contains predefined database query functions and their OpenAI tool definitions:
- `get_avg_salary_and_female_count_for_division(division_name)`
- `get_total_overtime_pay_for_department(department_name)`
- `get_total_longevity_pay_for_grade(grade)`
- `get_employee_count_by_gender_in_department(department_name)`
- `get_employees_with_overtime_above(amount)`

These functions use SQLAlchemy with raw SQL queries (vulnerable to SQL injection - for demo purposes only).

## Running the Applications

### Streamlit Web Interfaces

**CSV Agent (Pandas-based analysis)**:
```bash
cd database-ai-agents-main
streamlit run csv_agent.py
```

**SQL Agent (Natural language to SQL)**:
```bash
cd database-ai-agents-main
streamlit run sql_db_agent.py
```

### CLI Scripts

**Basic chat agent**:
```bash
cd database-ai-agents-main
python first_agent.py
```

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

## Model Configuration

All agents use `gpt-3.5-turbo` for cost efficiency. The model is initialized as:
```python
llm_name = "gpt-3.5-turbo"
model = ChatOpenAI(api_key=openai_key, model=llm_name)  # LangChain
# OR
client = OpenAI(api_key=openai_key)  # Direct OpenAI API
```

## Sample Questions

See `questions_sql_agent.md` for example queries organized by category:
- General aggregations (average salary, employee counts)
- Department-specific queries
- Gender-based comparisons
- Grade-specific analysis
- Complex multi-condition queries

## Important Notes

- The database is SQLite-based and recreated from CSV on each agent run (not persistent)
- SQL queries in helpers.py use string formatting (SQL injection vulnerable - demo code)
- All agents operate on the same `salaries_2023` table structure
- Streamlit apps run on default port 8501
