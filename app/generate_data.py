import csv
import random
from datetime import datetime, timedelta
from faker import Faker

from database import get_connection


fake = Faker("en_IN")
random.seed(42)
Faker.seed(42)


REGION_COUNT = 10
CUSTOMER_COUNT = 100_000
PRODUCT_COUNT = 10_000
SALES_COUNT = 1_000_000

BATCH_SIZE = 50_000


REGIONS = [
    "North",
    "South",
    "East",
    "West",
    "Central",
    "Northeast",
    "Northwest",
    "Southeast",
    "Southwest",
    "International",
]


PRODUCT_CATEGORIES = [
    "Computers",
    "Monitors",
    "Accessories",
    "Audio",
    "Tablets",
    "Networking",
    "Storage",
    "Software",
]


def generate_regions(connection):
    print("Generating regions...")

    rows = [
        (region_name,)
        for region_name in REGIONS
    ]

    with connection.cursor() as cursor:
        cursor.executemany(
            """
            INSERT INTO regions (region_name)
            VALUES (%s)
            """,
            rows,
        )

    connection.commit()

    print(f"Inserted {len(rows):,} regions.")


def generate_customers(connection):
    print("Generating customers...")

    with connection.cursor() as cursor:

        batch = []

        for i in range(CUSTOMER_COUNT):

            customer_name = fake.name()
            email = f"customer_{i + 1}@example.com"

            region_id = random.randint(1, REGION_COUNT)

            customer_type = random.choice(
                ["Enterprise", "SMB", "Mid-Market"]
            )

            created_at = fake.date_time_between(
                start_date="-3y",
                end_date="now",
            )

            batch.append(
                (
                    customer_name,
                    email,
                    region_id,
                    customer_type,
                    created_at,
                )
            )

            if len(batch) >= BATCH_SIZE:

                cursor.executemany(
                    """
                    INSERT INTO customers
                    (
                        customer_name,
                        email,
                        region_id,
                        customer_type,
                        created_at
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    batch,
                )

                connection.commit()

                print(
                    f"Customers inserted: "
                    f"{i + 1:,}/{CUSTOMER_COUNT:,}"
                )

                batch.clear()

        if batch:

            cursor.executemany(
                """
                INSERT INTO customers
                (
                    customer_name,
                    email,
                    region_id,
                    customer_type,
                    created_at
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                batch,
            )

            connection.commit()

    print(f"Inserted {CUSTOMER_COUNT:,} customers.")


def generate_products(connection):
    print("Generating products...")

    with connection.cursor() as cursor:

        batch = []

        for i in range(PRODUCT_COUNT):

            product_name = (
                f"{random.choice(PRODUCT_CATEGORIES)} "
                f"Product {i + 1}"
            )

            category = random.choice(PRODUCT_CATEGORIES)

            unit_price = round(
                random.uniform(500, 150000),
                2,
            )

            active = random.random() < 0.95

            batch.append(
                (
                    product_name,
                    category,
                    unit_price,
                    active,
                )
            )

            if len(batch) >= BATCH_SIZE:

                cursor.executemany(
                    """
                    INSERT INTO products
                    (
                        product_name,
                        category,
                        unit_price,
                        active
                    )
                    VALUES (%s, %s, %s, %s)
                    """,
                    batch,
                )

                connection.commit()

                print(
                    f"Products inserted: "
                    f"{i + 1:,}/{PRODUCT_COUNT:,}"
                )

                batch.clear()

        if batch:

            cursor.executemany(
                """
                INSERT INTO products
                (
                    product_name,
                    category,
                    unit_price,
                    active
                )
                VALUES (%s, %s, %s, %s)
                """,
                batch,
            )

            connection.commit()

    print(f"Inserted {PRODUCT_COUNT:,} products.")


def generate_sales(connection):
    print("Generating 1,000,000 sales records...")

    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 8, 15)

    total_days = (end_date - start_date).days

    with connection.cursor() as cursor:

        batch = []

        for i in range(SALES_COUNT):

            customer_id = random.randint(
                1,
                CUSTOMER_COUNT,
            )

            product_id = random.randint(
                1,
                PRODUCT_COUNT,
            )

            sale_date = (
                start_date
                + timedelta(
                    days=random.randint(0, total_days)
                )
            ).date()

            amount = round(
                random.uniform(500, 150000),
                2,
            )

            status = random.choices(
                ["completed", "cancelled", "returned"],
                weights=[90, 7, 3],
                k=1,
            )[0]

            batch.append(
                (
                    customer_id,
                    product_id,
                    amount,
                    sale_date,
                    status,
                )
            )

            if len(batch) >= BATCH_SIZE:

                cursor.executemany(
                    """
                    INSERT INTO sales
                    (
                        customer_id,
                        product_id,
                        amount,
                        sale_date,
                        status
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    batch,
                )

                connection.commit()

                print(
                    f"Sales inserted: "
                    f"{i + 1:,}/{SALES_COUNT:,}"
                )

                batch.clear()

        if batch:

            cursor.executemany(
                """
                INSERT INTO sales
                (
                    customer_id,
                    product_id,
                    amount,
                    sale_date,
                    status
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                batch,
            )

            connection.commit()

    print(f"Inserted {SALES_COUNT:,} sales.")


def main():
    connection = get_connection()

    try:
        generate_regions(connection)
        generate_customers(connection)
        generate_products(connection)
        generate_sales(connection)

        print("\nData generation completed successfully!")

    finally:
        connection.close()


if __name__ == "__main__":
    main()