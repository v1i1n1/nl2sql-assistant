from retrieval import retrieve_documents
from llm_service import generate_sql
from sql_executor import execute_sql
from answer_formatter import format_answer
from cache_service import get_cached_result, save_cached_result


def build_context(results):

    context_parts = []

    for row in results:

        document_id, source, content, distance = row

        context_parts.append(
            f"""
SOURCE: {source}

{content}
"""
        )

    return "\n".join(context_parts)


def generate_query(question: str):

    results = retrieve_documents(
        question,
        top_k=3
    )

    context = build_context(results)

    sql = generate_sql(
        question,
        context
    )

    return sql, results


def run_query(question: str):

    print("\nUSER QUESTION")
    print(question)

    # -------------------------
    # RAG RETRIEVAL
    # -------------------------

    sql, results = generate_query(question)

    print("\nRETRIEVED CONTEXT")

    for row in results:

        print(
            f"{row[1]} "
            f"(distance={row[3]:.6f})"
        )

    # -------------------------
    # GENERATED SQL
    # -------------------------

    print("\nGENERATED SQL")
    print(sql)

    # -------------------------
    # SQL EXECUTION
    # -------------------------

    print("\nEXECUTING SQL...")

    columns, rows = execute_sql(sql)

    print("\nRESULT")

    print(columns)

    for row in rows:
        print(row)

    answer = format_answer(
        question,
        columns,
        rows
    )
    
    print("\nFINAL ANSWER")
    print(answer)
    
    return columns, rows


if __name__ == "__main__":

    question = "Which region generated the highest sales?"

    run_query(question)