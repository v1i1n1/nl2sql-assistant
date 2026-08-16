from llm_service import generate_sql


def main():

    context = """
TABLE: sales

COLUMNS:
sale_id
customer_id
product_id
amount
sale_date
status

TABLE: customers

COLUMNS:
customer_id
customer_name
region_id

TABLE: regions

COLUMNS:
region_id
region_name

RELATIONSHIPS:

sales.customer_id -> customers.customer_id
customers.region_id -> regions.region_id

BUSINESS RULE:

Revenue and sales calculations should use
completed transactions only.
"""

    question = "Which region generated the highest sales, and what was the total sales amount?"

    sql = generate_sql(
        question,
        context
    )

    print("\nGENERATED SQL:\n")
    print(sql)


if __name__ == "__main__":
    main()