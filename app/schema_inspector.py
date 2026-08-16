from database import get_connection


def get_schema():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    table_name,
                    column_name,
                    data_type,
                    is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'public'
                ORDER BY table_name, ordinal_position;
            """)

            rows = cursor.fetchall()

            schema = {}

            for table_name, column_name, data_type, is_nullable in rows:

                if table_name not in schema:
                    schema[table_name] = []

                schema[table_name].append({
                    "column": column_name,
                    "data_type": data_type,
                    "nullable": is_nullable
                })

            return schema

    finally:
        connection.close()


def get_relationships():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT
                    tc.table_name AS source_table,
                    kcu.column_name AS source_column,
                    ccu.table_name AS target_table,
                    ccu.column_name AS target_column
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                    AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY'
                  AND tc.table_schema = 'public'
                ORDER BY tc.table_name, kcu.column_name;
            """)

            return cursor.fetchall()

    finally:
        connection.close()


if __name__ == "__main__":

    schema = get_schema()

    print("DATABASE SCHEMA")

    for table_name, columns in schema.items():

        print(f"\nTABLE: {table_name}")

        for column in columns:

            print(
                f"  - {column['column']} "
                f"| {column['data_type']} "
                f"| nullable={column['nullable']}"
            )

    relationships = get_relationships()

    print("\nFOREIGN KEY RELATIONSHIPS")

    for relationship in relationships:

        source_table, source_column, target_table, target_column = relationship

        print(
            f"  - {source_table}.{source_column}"
            f" -> "
            f"{target_table}.{target_column}"
        )