from embedding_service import create_embedding


def main():

    text = "sales table contains customer transactions"

    embedding = create_embedding(text)

    print("Embedding created successfully!")
    print("Embedding dimensions:", len(embedding))
    print("First 5 values:", embedding[:5])


if __name__ == "__main__":
    main()