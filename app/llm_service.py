import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_sql(question: str, context: str) -> str:

    prompt = f"""
You are an expert PostgreSQL SQL generator.

Convert the user's natural language question into a valid
PostgreSQL SQL query.

STRICT RULES:

1. Use ONLY tables and columns provided in the database context.
2. Do not invent tables, columns, relationships, or values.
3. Follow all business rules provided in the context.
4. Revenue and sales calculations must use completed transactions
   when the business rule specifies this.
5. For ranking questions, return both the entity and the metric
   used for ranking whenever appropriate.
6. Use meaningful column aliases such as total_sales, total_spent,
   transaction_count, or average_amount.
7. Return ONLY SQL.
8. Do not use markdown code fences.
9. Generate read-only SELECT queries only.

DATABASE CONTEXT:
{context}

USER QUESTION:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You generate accurate PostgreSQL SQL."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()