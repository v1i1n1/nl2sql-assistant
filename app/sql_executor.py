from database import get_connection


FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE",
]


def validate_sql(sql: str) -> bool:

    normalized_sql = sql.strip().upper()

    if not normalized_sql.startswith("SELECT"):
        raise ValueError(
            "Only SELECT queries are allowed."
        )

    for keyword in FORBIDDEN_KEYWORDS:

        if keyword in normalized_sql:
            raise ValueError(
                f"Forbidden SQL operation detected: {keyword}"
            )

    return True


def execute_sql(sql: str):

    validate_sql(sql)

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(sql)

            columns = [
                description[0]
                for description in cursor.description
            ]

            rows = cursor.fetchall()

            return columns, rows

    finally:
        connection.close()