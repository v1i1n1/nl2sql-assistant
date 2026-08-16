import json
from pathlib import Path

from database import get_connection
from embedding_service import create_embedding


PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"


def load_documents():
    documents = []

    for file_path in KNOWLEDGE_DIR.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")

        documents.append(
            {
                "content": content,
                "source": file_path.name,
            }
        )

    return documents


def insert_document(connection, document):
    embedding = create_embedding(document["content"])

    metadata = {
        "type": "schema",
        "source": document["source"],
    }

    embedding_string = "[" + ",".join(
        str(value) for value in embedding
    ) + "]"

    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO knowledge_embeddings
            (
                content,
                source,
                metadata,
                embedding
            )
            VALUES (%s, %s, %s, %s::vector)
            """,
            (
                document["content"],
                document["source"],
                json.dumps(metadata),
                embedding_string,
            ),
        )

    connection.commit()


def main():
    documents = load_documents()

    print(f"Found {len(documents)} knowledge documents.")

    connection = get_connection()

    try:
        for document in documents:
            print(f"Embedding: {document['source']}")

            insert_document(
                connection,
                document,
            )

            print(f"Inserted: {document['source']}")

    finally:
        connection.close()

    print("\nKnowledge ingestion completed successfully!")


if __name__ == "__main__":
    main()