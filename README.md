````markdown
# NL2SQL Assistant

A RAG-powered Natural Language to SQL Assistant that allows users to ask questions about business data using natural language.

The system retrieves relevant database schema information using vector similarity search, generates PostgreSQL SQL using an LLM, validates the generated SQL, executes it against PostgreSQL, and returns the result as a natural-language answer.

---

## 🚀 Project Overview

Traditional database querying requires users to know SQL.

This project allows users to ask questions such as:

> Which region generated the highest sales?

Instead of manually writing SQL, the assistant automatically:

1. Understands the user's question
2. Retrieves relevant database schema information
3. Generates PostgreSQL SQL
4. Validates the SQL for read-only execution
5. Executes the SQL against PostgreSQL
6. Returns the database result
7. Presents the result in natural language

---

## 🏗️ Architecture

```text
                    User
                     │
                     ▼
             Natural Language
                Question
                     │
                     ▼
            OpenAI Embedding
                     │
                     ▼
          PostgreSQL + pgvector
                     │
                     ▼
          Semantic Schema Retrieval
                     │
                     ▼
             Relevant Context
                     │
                     ▼
                 LLM
                     │
                     ▼
             SQL Generation
                     │
                     ▼
             SQL Validation
                     │
                     ▼
              PostgreSQL
                     │
                     ▼
               Query Result
                     │
                     ▼
        Natural Language Answer
                     │
                     ▼
                  Web UI
````

---

## ✨ Features

* Natural language database querying
* RAG-based schema retrieval
* PostgreSQL integration
* pgvector semantic similarity search
* OpenAI embeddings
* LLM-powered SQL generation
* Schema-aware SQL generation
* Business-rule-aware SQL generation
* Read-only SQL validation
* PostgreSQL query execution
* Natural-language answer formatting
* FastAPI REST API
* Interactive Swagger API documentation
* Web-based user interface
* Synthetic large-scale dataset generation using Faker
* Support for a 1-million-record sales dataset

---

## 🛠️ Technology Stack

| Technology          | Purpose                   |
| ------------------- | ------------------------- |
| Python              | Application development   |
| PostgreSQL          | Relational database       |
| pgvector            | Vector similarity search  |
| OpenAI              | Embeddings and LLM        |
| FastAPI             | Backend REST API          |
| Psycopg             | PostgreSQL connectivity   |
| Faker               | Synthetic data generation |
| HTML/CSS/JavaScript | Web UI                    |
| RAG                 | Schema retrieval          |

---

## 📊 Database

The project uses PostgreSQL with the following business tables:

```text
regions
customers
products
sales
```

### Dataset Size

```text
Regions       : 10
Customers     : 100,000
Products      : 10,000
Sales         : 1,000,000
```

The project also contains a vector knowledge table:

```text
knowledge_embeddings
```

This table stores the embedded database schema and business-rule documents.

---

## 🗄️ Database Schema

### Regions

```text
region_id
region_name
```

Relationship:

```text
regions.region_id
        ↑
customers.region_id
```

---

### Customers

```text
customer_id
customer_name
email
region_id
customer_type
created_at
```

Relationship:

```text
customers.region_id
        ↓
regions.region_id
```

---

### Products

```text
product_id
product_name
category
unit_price
active
```

---

### Sales

```text
sale_id
customer_id
product_id
amount
sale_date
status
```

Relationships:

```text
sales.customer_id
        ↓
customers.customer_id

sales.product_id
        ↓
products.product_id
```

---

## 🧠 RAG Knowledge Layer

Database schema information is stored as knowledge documents.

Example:

```text
knowledge/
├── customers_schema.txt
├── products_schema.txt
├── regions_schema.txt
└── sales_schema.txt
```

These documents contain:

* Table descriptions
* Column descriptions
* Relationships
* Business rules

The documents are converted into 1536-dimensional embeddings and stored in PostgreSQL using pgvector.

```text
Knowledge Document
       ↓
OpenAI Embedding
       ↓
1536-dimensional vector
       ↓
PostgreSQL
       ↓
knowledge_embeddings
```

---

## 🔍 Semantic Retrieval

When a user asks a question, the question is converted into an embedding.

The system performs vector similarity search using pgvector.

Example:

```text
Question:

Which table contains customer transactions,
transaction amount and status?
```

The retrieval system identifies:

```text
sales_schema.txt
customers_schema.txt
regions_schema.txt
```

The most relevant schema is then provided to the LLM.

---

## 🤖 SQL Generation

The LLM receives:

```text
User Question
+
Retrieved Database Schema
+
Business Rules
```

and generates PostgreSQL SQL.

Example question:

```text
Which region generated the highest sales?
```

Generated SQL:

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

---

## 🔒 SQL Safety

The project contains a SQL validation layer.

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

Example:

```text
SELECT 1;
```

Result:

```text
Allowed
```

Example:

```text
DROP TABLE sales;
```

Result:

```text
Rejected
```

This prevents destructive SQL generated by the LLM from being executed.

---

## 🧪 Example End-to-End Flow

### User Question

```text
Which region generated the highest sales?
```

### Retrieved Context

```text
regions_schema.txt
sales_schema.txt
customers_schema.txt
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

### Database Result

```text
Southeast
6,898,582,484.18
```

### Final Answer

```text
Southeast has the highest sales with 6,898,582,484.18.
```

---

## 📁 Project Structure

```text
NL2SQL-Assistant/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── embedding_service.py
│   ├── generate_data.py
│   ├── ingest_knowledge.py
│   ├── llm_service.py
│   ├── main.py
│   ├── nl2sql_pipeline.py
│   ├── retrieval.py
│   ├── schema_inspector.py
│   ├── sql_executor.py
│   ├── answer_formatter.py
│   ├── test_db.py
│   ├── test_embedding.py
│   └── test_llm.py
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

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/v1i1n1/nl2sql-assistant.git
cd nl2sql-assistant
```

---

### 2. Create a virtual environment

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

---

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 🐘 PostgreSQL Setup

Make sure PostgreSQL is installed and running.

Create the database:

```sql
CREATE DATABASE nl2sql_db;
```

Connect to it:

```text
nl2sql_db
```

The project uses:

```text
Host     : localhost
Port     : 5432
Database : nl2sql_db
User     : postgres
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root.

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nl2sql_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password

OPENAI_API_KEY=your_openai_api_key
```

### Important

Never commit `.env` to GitHub.

The `.gitignore` file excludes it from version control.

---

## 📦 Generate Synthetic Data

The project includes a Faker-based data generation script.

From the `app` directory:

```powershell
python generate_data.py
```

The script generates:

```text
10 regions
100,000 customers
10,000 products
1,000,000 sales
```

---

## 🧠 Enable pgvector

The project uses PostgreSQL's pgvector extension.

Inside `nl2sql_db`:

```sql
CREATE EXTENSION vector;
```

Verify:

```sql
\dx
```

You should see:

```text
vector
```

---

## 📚 Ingest Knowledge

After the knowledge documents are available:

```powershell
python ingest_knowledge.py
```

Verify the embeddings:

```sql
SELECT
    source,
    vector_dims(embedding)
FROM knowledge_embeddings;
```

Expected dimension:

```text
1536
```

---

## 🔎 Test Semantic Retrieval

Run:

```powershell
python retrieval.py
```

The system retrieves the most relevant schema documents for a natural-language question.

---

## 🤖 Test LLM SQL Generation

Run:

```powershell
python test_llm.py
```

This verifies that the LLM can generate PostgreSQL SQL using the provided schema context.

---

## 🔄 Test Complete NL2SQL Pipeline

Run:

```powershell
python nl2sql_pipeline.py
```

The complete flow is:

```text
Question
   ↓
Embedding
   ↓
RAG Retrieval
   ↓
LLM SQL Generation
   ↓
SQL Validation
   ↓
PostgreSQL Execution
   ↓
Answer
```

---

## 🚀 Run FastAPI

From the `app` directory:

```powershell
uvicorn main:app --reload
```

The application will start at:

```text
http://127.0.0.1:8000
```

---

## 📖 API Documentation

FastAPI automatically provides Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

### Endpoint

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

After starting FastAPI:

```powershell
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

The UI allows users to:

* Enter natural-language questions
* Submit questions to the API
* View generated SQL
* View database results
* View the final natural-language answer

---

## 🧪 Example Questions

The assistant can handle questions such as:

```text
Which region generated the highest sales?
```

```text
Which product generated the highest sales?
```

```text
Which customer spent the most?
```

```text
How many completed sales transactions are there?
```

```text
What is the total amount of completed sales?
```

```text
What were the total completed sales in July 2026?
```

```text
Which region had the highest completed sales in July 2026?
```

```text
Show the total completed sales for each region.
```

---

## 🔐 Security Considerations

* API keys are stored in environment variables.
* `.env` is excluded from Git.
* SQL execution is restricted to read-only queries.
* Destructive SQL operations are rejected before execution.
* The LLM is instructed to use only retrieved schema information.

---

## 📈 Future Improvements

Potential enhancements include:

* Improved SQL validation
* Better handling of ambiguous questions
* Query retry and correction
* Conversation memory
* Query history
* Authentication
* Better natural-language answer generation
* Result visualization and charts
* Query performance optimization
* Production deployment
* Improved schema retrieval using relationship-aware retrieval

---

## 👨‍💻 Project

**NL2SQL Assistant**

A practical implementation of:

```text
RAG
+
LLM
+
PostgreSQL
+
pgvector
+
FastAPI
+
Natural Language SQL
```

---

## 📌 Version

```text
Version: 1.0
Status: Working End-to-End
```

````

### Then save it as:

```text
F:\NL2SQL-Assistant\README.md
````

After saving, buddy, because your previous commit was already created, run in the **VS Code terminal**:

```powershell
git status
git add README.md
git commit -m "Add project README"
git push
```

