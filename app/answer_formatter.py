def format_answer(question, columns, rows):

    if not rows:
        return "No results found for your question."

    if len(rows) == 1:

        row = rows[0]

        if len(columns) == 1:
            return f"The answer is {row[0]}."

        if len(columns) == 2:
            return (
                f"{row[0]} has the highest value with "
                f"{row[1]:,.2f}."
            )

    return "\n".join(
        " | ".join(
            str(value) for value in row
        )
        for row in rows
    )