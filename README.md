````markdown
# 🤖 NL2SQL Assistant

An agentic Natural Language-to-SQL Assistant that converts natural-language business questions into safe, executable PostgreSQL queries and returns business-friendly answers.

The project combines **RAG, PostgreSQL, pgvector, OpenAI, Google ADK, LangGraph, PostgreSQL caching, FastAPI, and DeepEval** into an end-to-end NL2SQL system.

---

## 🚀 Project Overview

The NL2SQL Assistant allows users to ask questions such as:

- Which region generated the highest sales?
- Which region has the most customers?
- Which product generated the highest sales?

Instead of manually writing SQL, the system:

1. Understands the user's natural-language question
2. Retrieves relevant database schema using vector similarity search
3. Generates PostgreSQL SQL
4. Validates the SQL for safety
5. Executes the query against PostgreSQL
6. Caches the result for repeated questions
7. Converts the database result into a natural-language answer
8. Evaluates the system using DeepEval

---

## 🏗️ Architecture

```text
                         USER
                           │
                           ▼
                    ┌─────────────┐
                    │   FastAPI   │
                    │   Web UI    │
                    └──────┬──────┘
                           │
                           ▼
                 ┌──────────────────┐
                 │   Google ADK     │
                 │      Agent       │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │    LangGraph     │
                 │     Workflow     │
                 └────────┬─────────┘
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
    Schema Retrieval  SQL Generation  SQL Validation
          │               │                │
          ▼               ▼                │
   PostgreSQL +      GPT-4.1-mini         │
      pgvector                            │
          │                                │
          └───────────────┬────────────────┘
                          ▼
                  ┌───────────────┐
                  │ SQL Execution │
                  └───────┬───────┘
                          │
                          ▼
                    PostgreSQL
                          │
                          ▼
                  ┌───────────────┐
                  │ Answer        │
                  │ Formatting    │
                  └───────┬───────┘
                          │
                          ▼
                  PostgreSQL Cache
                          │
                          ▼
                    Final Answer

                    ┌───────────┐
                    │ DeepEval  │
                    │ Evaluation│
                    └───────────┘
````

---

## ✨ Key Features

### 🔹 Natural Language to SQL

Users can ask database questions using normal business language without knowing SQL.

### 🔹 RAG-Based Schema Retrieval

Relevant database schema and business rules are retrieved using semantic similarity search before SQL generation.

### 🔹 PostgreSQL + pgvector

PostgreSQL stores both application data and vector embeddings.

`pgvector` is used for semantic similarity search over the knowledge base.

### 🔹 OpenAI Embeddings

The project uses OpenAI embeddings with **1536-dimensional vectors** for schema retrieval.

### 🔹 GPT-4.1-mini

GPT-4.1-mini is used to generate PostgreSQL SQL queries from the user's question and retrieved database context.

### 🔹 SQL Safety Validation

Only read-only `SELECT` queries are allowed.

The system blocks operations such as:

```text
INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE
CREATE
GRANT
REVOKE
```

### 🔹 Google ADK

Google Agent Development Kit is used to create the agent layer and expose database capabilities as tools.

ADK tools include:

* Schema retrieval
* SQL generation
* SQL validation
* SQL execution

### 🔹 LangGraph

LangGraph manages the state-based NL2SQL workflow:

```text
START
  ↓
Retrieve Schema
  ↓
Generate SQL
  ↓
Validate SQL
  ↓
Execute SQL
  ↓
Format Answer
  ↓
END
```

### 🔹 PostgreSQL Query Caching

Previously executed questions and results can be stored in PostgreSQL.

For repeated questions:

```text
User Question
      ↓
Cache Check
   ↙       ↘
 HIT       MISS
  ↓          ↓
Return    NL2SQL Pipeline
Result        ↓
           PostgreSQL
              ↓
           Save Cache
```

### 🔹 FastAPI

FastAPI provides the REST API layer for the NL2SQL assistant.

### 🔹 Interactive Web UI

The project includes a simple web interface where users can:

* Enter natural-language questions
* Submit questions
* View generated SQL
* View database results
* View final answers

### 🔹 DeepEval

DeepEval is used to evaluate the quality of the NL2SQL/RAG pipeline.

Evaluation metrics include:

* NL2SQL Answer Correctness
* Answer Relevancy
* Contextual Relevancy

---

## 🗂️ Project Structure

```text
NL2SQL-Assistant/
│
├── app/
│   │
│   ├── adk_agent/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── tools.py
│   │
│   ├── agentic_pipeline.py
│   ├── answer_formatter.py
│   ├── cache_service.py
│   ├── database.py
│   ├── embedding_service.py
│   ├── llm_service.py
│   ├── main.py
│   ├── nl2sql_pipeline.py
│   ├── retrieval.py
│   ├── sql_executor.py
│   └── test_deepeval.py
│
├── knowledge/
│   ├── customers_schema.txt
│   ├── products_schema.txt
│   ├── regions_schema.txt
│   └── sales_schema.txt
│
├── static/
│   └── index.html
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🧠 Database Knowledge Base

The project currently uses four schema documents:

```text
customers_schema.txt
products_schema.txt
regions_schema.txt
sales_schema.txt
```

These documents contain:

* Table descriptions
* Column definitions
* Relationships
* Business rules

For example, the sales schema contains the business rule that revenue calculations should use completed transactions.

---

## 🗄️ PostgreSQL Database

The project uses PostgreSQL with the `pgvector` extension.

### Enable pgvector

```sql
CREATE EXTENSION vector;
```

### Knowledge Embedding Table

```sql
CREATE TABLE knowledge_embeddings (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    source TEXT NOT NULL,
    metadata JSONB,
    embedding VECTOR(1536),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

The schema documents are converted into embeddings and stored in this table.

---

## 🔍 Semantic Retrieval

When the user asks a question:

```text
User Question
      ↓
Create Query Embedding
      ↓
pgvector Similarity Search
      ↓
Top-K Relevant Documents
      ↓
Database Context
```

The project uses pgvector distance search:

```sql
ORDER BY embedding <=> query_embedding
LIMIT 3;
```

---

## 🧮 Example Query

### User Question

```text
Which region generated the highest sales?
```

### Generated SQL

```sql
SELECT
    r.region_name,
    SUM(s.amount) AS total_sales
FROM sales s
JOIN customers c
    ON s.customer_id = c.customer_id
JOIN regions r
    ON c.region_id = r.region_id
WHERE s.status = 'completed'
GROUP BY r.region_name
ORDER BY total_sales DESC
LIMIT 1;
```

### Result

```text
Southeast
6,898,582,484.18
```

### Final Answer

```text
Southeast has the highest value with 6,898,582,484.18.
```

---

## 🛡️ SQL Security

The generated SQL is validated before execution.

Only queries beginning with:

```sql
SELECT
```

are allowed.

Destructive operations are rejected before they reach PostgreSQL.

Example:

```text
DROP TABLE sales;
```

Result:

```text
ValueError: Only SELECT queries are allowed.
```

---

## 🤖 Google ADK Agent

The ADK agent exposes the following tools:

```text
retrieve_schema()
        ↓
generate_database_sql()
        ↓
validate_database_sql()
        ↓
execute_database_sql()
```

The ADK Web interface can be started using:

```powershell
adk web
```

Open:

```text
http://127.0.0.1:8000
```

---

## 🔄 LangGraph Workflow

The LangGraph workflow is implemented using a state-based graph.

```text
START
  │
  ▼
retrieve
  │
  ▼
generate_sql
  │
  ▼
validate_sql
  │
  ▼
execute_sql
  │
  ▼
format_answer
  │
  ▼
END
```

Run the LangGraph pipeline:

```powershell
cd F:\NL2SQL-Assistant\app
python agentic_pipeline.py
```

---

## ⚡ PostgreSQL Caching

The project includes a PostgreSQL-backed cache.

Cached information includes:

```text
question
sql
answer
columns
rows
created_at
last_used_at
```

This reduces unnecessary repeated processing for previously asked questions.

---

## 🌐 FastAPI

Start the FastAPI application:

```powershell
cd F:\NL2SQL-Assistant\app
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

### API Endpoint

```text
POST /ask
```

Example request:

```json
{
    "question": "Which region generated the highest sales?"
}
```

Example response:

```json
{
    "question": "Which region generated the highest sales?",
    "sql": "SELECT ...",
    "answer": "Southeast has the highest value with 6898582484.18.",
    "columns": [
        "region_name",
        "total_sales"
    ],
    "rows": [
        [
            "Southeast",
            6898582484.18
        ]
    ]
}
```

---

## 🖥️ Web UI

The web UI allows users to:

* Enter natural-language questions
* Submit questions to the API
* View generated SQL
* View database results
* View the final natural-language answer

Start FastAPI:

```powershell
uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

---

## 📊 DeepEval Evaluation

DeepEval is used to evaluate the NL2SQL pipeline using three test cases.

### Test Questions

```text
1. Which region generated the highest sales?

2. Which region has the most customers?

3. Which product generated the highest sales?
```

### Evaluation Results

| Metric                    | Average Score |  Pass Rate |
| ------------------------- | ------------: | ---------: |
| NL2SQL Answer Correctness |      **1.00** |   **100%** |
| Answer Relevancy          |      **0.83** | **66.67%** |
| Contextual Relevancy      |      **0.46** |     **0%** |

### Interpretation

**NL2SQL Answer Correctness: 1.00**

All three test cases produced the expected answers.

**Answer Relevancy: 0.83**

The generated answers were generally relevant to the questions.

**Contextual Relevancy: 0.46**

This indicates an area for future RAG optimization. The current retrieval can return additional schema information that is not directly required for a specific question.

### Run Evaluation

```powershell
cd F:\NL2SQL-Assistant\app
python test_deepeval.py
```

---

## ⚙️ Installation

### 1. Clone the repository

```powershell
git clone https://github.com/v1i1n1/nl2sql-assistant.git
```

```powershell
cd nl2sql-assistant
```

### 2. Create virtual environment

```powershell
python -m venv venv
```

### 3. Activate virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root.

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nl2sql_db
DB_USER=postgres
DB_PASSWORD=your_password

OPENAI_API_KEY=your_openai_api_key

GOOGLE_API_KEY=your_google_api_key
```

### Important

Never commit `.env` to GitHub.

The project includes `.env` in `.gitignore`.

---

## 🧪 Testing

### Test Embeddings

```powershell
python test_embedding.py
```

### Test Retrieval

```powershell
python retrieval.py
```

### Test SQL Generation

```powershell
python test_llm.py
```

### Test Full NL2SQL Pipeline

```powershell
python nl2sql_pipeline.py
```

### Test SQL Validation

```powershell
python -c "from sql_executor import validate_sql; print(validate_sql('SELECT 1;'))"
```

### Test LangGraph

```powershell
python agentic_pipeline.py
```

### Test DeepEval

```powershell
python test_deepeval.py
```

### Run Google ADK

```powershell
adk web
```

---

## 🛠️ Technology Stack

| Technology          | Purpose                  |
| ------------------- | ------------------------ |
| Python              | Application development  |
| PostgreSQL          | Relational database      |
| pgvector            | Vector similarity search |
| OpenAI Embeddings   | Schema embeddings        |
| GPT-4.1-mini        | SQL generation           |
| Google ADK          | Agent orchestration      |
| LangGraph           | Workflow orchestration   |
| FastAPI             | REST API                 |
| HTML/CSS/JavaScript | Web UI                   |
| DeepEval            | LLM/RAG evaluation       |
| Git/GitHub          | Version control          |

---

## 🔮 Future Improvements

Potential future enhancements include:

* Improve schema chunking for better contextual retrieval
* Improve answer formatting based on column semantics
* Add SQL retry and correction workflows
* Add more comprehensive evaluation datasets
* Add authentication and authorization
* Add Docker deployment
* Add production monitoring
* Add more advanced multi-agent workflows
* Improve cache invalidation strategies
* Deploy the application to AWS

---

## 🎯 Project Highlights

This project demonstrates an end-to-end **agentic NL2SQL architecture** combining:

```text
RAG
+
Vector Search
+
LLM SQL Generation
+
SQL Safety
+
LangGraph
+
Google ADK
+
PostgreSQL Caching
+
FastAPI
+
DeepEval
```

The system is designed to safely transform natural-language business questions into executable PostgreSQL queries while grounding SQL generation in the database schema and business rules.

---

## 👨‍💻 Author

**Vinod Raj**

AI / ML | Generative AI | RAG | LLM Applications | Agentic AI

---

## 📄 License

This project is intended for learning, demonstration, and portfolio purposes.


