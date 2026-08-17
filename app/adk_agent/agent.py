from google.adk.agents import Agent

from .tools import (
    retrieve_schema,
    generate_database_sql,
    validate_database_sql,
    execute_database_sql,
)


root_agent = Agent(
    name="nl2sql_agent",
    model="gemini-3.6-flash",
    instruction="""
You are an NL2SQL database assistant.

Your job is to answer user questions about the PostgreSQL
business database.

Follow this workflow:

1. Retrieve the relevant database schema using retrieve_schema.
2. Generate SQL using generate_database_sql.
3. Validate the SQL using validate_database_sql.
4. Execute the validated SQL using execute_database_sql.
5. Return a concise business-friendly answer.

Important rules:

- Never invent tables or columns.
- Use only information from retrieved schema context.
- Only read-only SELECT queries are allowed.
- Never execute INSERT, UPDATE, DELETE, DROP, ALTER,
  TRUNCATE, CREATE, GRANT, or REVOKE.
- Follow business rules contained in the retrieved schema.
""",
    tools=[
        retrieve_schema,
        generate_database_sql,
        validate_database_sql,
        execute_database_sql,
    ],
)