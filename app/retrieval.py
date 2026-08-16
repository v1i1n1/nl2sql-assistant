from database import get_connection
from embedding_service import create_embedding


def retrieve_documents(question: str, top_k: int = 3):
    question_embedding = create_embedding(question)

    embedding_string = "[" + ",".join(
        str(value) for value in question_embedding
    ) + "]"

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    id,
                    source,
                    content,
                    embedding <=> %s::vector AS distance
                FROM knowledge_embeddings
                ORDER BY embedding <=> %s::vector
                LIMIT %s;
                """,
                (
                    embedding_string,
                    embedding_string,
                    top_k,
                ),
            )

            return cursor.fetchall()

    finally:
        connection.close()


if __name__ == "__main__":

    question = "Which table contains customer transactions, transaction amount and status?"

    results = retrieve_documents(question)

    print("\nRETRIEVED DOCUMENTS\n")

    for row in results:

        document_id, source, content, distance = row

        print(f"ID: {document_id}")
        print(f"Source: {source}")
        print(f"Distance: {distance:.6f}")
        print("-" * 60)
        print(content)
        print("=" * 60)