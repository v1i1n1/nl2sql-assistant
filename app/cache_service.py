import json

from database import get_connection


def get_cached_result(question: str):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    sql,
                    answer,
                    columns,
                    rows
                FROM nl2sql_cache
                WHERE question = %s;
                """,
                (question.strip(),)
            )

            result = cursor.fetchone()

            if not result:
                return None

            cursor.execute(
                """
                UPDATE nl2sql_cache
                SET last_used_at = CURRENT_TIMESTAMP
                WHERE question = %s;
                """,
                (question.strip(),)
            )

            connection.commit()

            sql, answer, columns, rows = result

            return {
                "sql": sql,
                "answer": answer,
                "columns": columns,
                "rows": rows
            }

    finally:
        connection.close()


def save_cached_result(
    question: str,
    sql: str,
    answer: str,
    columns,
    rows
):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO nl2sql_cache
                (
                    question,
                    sql,
                    answer,
                    columns,
                    rows
                )
                VALUES (%s, %s, %s, %s::jsonb, %s::jsonb)
                ON CONFLICT (question)
                DO UPDATE SET
                    sql = EXCLUDED.sql,
                    answer = EXCLUDED.answer,
                    columns = EXCLUDED.columns,
                    rows = EXCLUDED.rows,
                    last_used_at = CURRENT_TIMESTAMP;
                """,
                (
                    question.strip(),
                    sql,
                    answer,
                    json.dumps(columns),
                    json.dumps(rows, default=str)
                )
            )

        connection.commit()

    finally:
        connection.close()