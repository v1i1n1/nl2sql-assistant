from retrieval import retrieve_documents
from llm_service import generate_sql
from sql_executor import validate_sql, execute_sql
from answer_formatter import format_answer


def retrieve_schema(question: str) -> str:
    """
    Retrieve the most relevant database schema and business-rule
    documents for a user's natural-language question.
    """

    documents = retrieve_documents(question)

    context_parts = []

    for document_id, source, content, distance in documents:
        context_parts.append(
            f"Source: {source}\n"
            f"Content:\n{content}\n"
            f"Distance: {distance:.6f}"
        )

    return "\n\n" + ("\n\n" + "=" * 60 + "\n\n").join(
        context_parts
    )


def generate_database_sql(question: str, context: str) -> str:
    """
    Generate a read-only PostgreSQL SELECT query using the
    user's question and retrieved database schema context.
    """

    return generate_sql(question, context)


def validate_database_sql(sql: str) -> str:
    """
    Validate generated SQL and reject destructive database operations.
    Only SELECT queries are permitted.
    """

    validate_sql(sql)

    return "SQL validation successful. Query is read-only."


def execute_database_sql(sql: str) -> str:
    """
    Execute a validated read-only SQL query against PostgreSQL
    and return the query results.
    """

    columns, rows = execute_sql(sql)

    return format_answer(
        "",
        columns,
        rows
    )