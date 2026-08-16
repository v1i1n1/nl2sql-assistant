from database import get_connection


def main():
    connection = get_connection()

    print("Database connection successful!")

    with connection.cursor() as cursor:
        cursor.execute("SELECT current_database();")
        result = cursor.fetchone()

        print("Connected database:", result[0])

    connection.close()


if __name__ == "__main__":
    main()